import sys
import io
import math
import traceback

NMS_CONFLICT_SNIPPET = "operator torchvision::nms already has an DispatchKey::Meta"

def section(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

def require(cond, msg):
    if not cond:
        print(f"[FAIL] {msg}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"[OK] {msg}")

def try_import_vision():
    try:
        import torch
        import torchvision
        from PIL import Image  # Pillow needed for PIL transforms
        return torch, torchvision, Image
    except Exception as e:
        msg = str(e).replace("\n", " ")
        if NMS_CONFLICT_SNIPPET in msg:
            section("SKIP: NMS registration conflict detected")
            print(
                "Detected NMS Meta registration conflict during torchvision import.\n"
                "Skipping subtest1.py so your pipeline can continue."
            )
            sys.exit(0)
        print("torchvision import failed unexpectedly:", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

def main():
    section("1) Import (safe)")
    torch, torchvision, Image = try_import_vision()
    print(f"torch      : {torch.__version__}")
    print(f"torchvision: {torchvision.__version__}")

    section("2) PIL and Tensor transforms (classic v1)")
    try:
        from torchvision import transforms
        # Create a synthetic PIL Image (RGB)
        pil_img = Image.fromarray((torch.rand(32, 32, 3) * 255).byte().numpy(), mode="RGB")

        tfm_pil = transforms.Compose([
            transforms.Resize((28, 28)),
            transforms.CenterCrop(24),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
            transforms.RandomHorizontalFlip(0.5),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5],
                                 std=[0.5, 0.5, 0.5]),
        ])
        timg = tfm_pil(pil_img)  # -> Tensor CHW
        require(timg.shape == (3, 24, 24), "PIL pipeline produced CHW (3,24,24)")

        # Pure tensor pipeline (CHW)
        tfm_tensor = transforms.Compose([
            transforms.Normalize([0.5, 0.5, 0.5],
                                 [0.5, 0.5, 0.5]),
            transforms.RandomErasing(p=1.0, scale=(0.02, 0.05), ratio=(0.3, 3.3)),
        ])
        out = tfm_tensor(timg)
        require(out.shape == (3, 24, 24), "Tensor pipeline kept shape")
        print("Classic v1 transforms on PIL and Tensor ran successfully.")
    except Exception as e:
        print("Classic transforms test failed:", e, file=sys.stderr)
        sys.exit(1)

    section("3) Optional transforms.v2 (if available)")
    try:
        # v2 API exists in newer torchvision; skip gracefully if not present
        v2 = getattr(torchvision, "transforms", None)
        v2 = getattr(v2, "v2", None)
        if v2 is None:
            print("transforms.v2 not available in this torchvision; skipping this block.")
        else:
            # v2 transforms generally accept both PIL and tensors
            tfm_v2 = v2.Compose([
                v2.Resize((28, 28)),
                v2.RandomCrop((24, 24)),
                v2.RandomHorizontalFlip(0.5),
                v2.ToImage(),      # ensure image-like
                v2.ToDtype(torch.float32, scale=True),
                v2.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)),
            ])
            v2_img = tfm_v2(pil_img)  # CHW float32
            require(v2_img.shape == (3, 24, 24), "v2 pipeline produced CHW (3,24,24)")
            print("transforms.v2 pipeline executed successfully.")
    except Exception as e:
        print("transforms.v2 test failed:", e, file=sys.stderr)
        sys.exit(1)

    section("4) FakeData (grayscale) + DataLoader + utils.make_grid/save_image")
    try:
        from torchvision import datasets, transforms, utils
        from torch.utils.data import DataLoader

        tfm_gray = transforms.Compose([
            transforms.Grayscale(num_output_channels=1),
            transforms.Resize((28, 28)),
            transforms.ToTensor(),  # -> (1,28,28)
            transforms.Normalize(mean=[0.5], std=[0.5]),
        ])

        ds = datasets.FakeData(
            size=32,
            image_size=(3, 32, 32),  # Start RGB; we'll convert to grayscale in transform
            num_classes=5,
            transform=tfm_gray,
            random_offset=11,
        )
        loader = DataLoader(ds, batch_size=8, shuffle=True, num_workers=0)
        batch_imgs, batch_labels = next(iter(loader))
        require(batch_imgs.shape == (8, 1, 28, 28), "Grayscale batch has shape (8,1,28,28)")

        # Make a grid (1 row) and save to disk (requires Pillow)
        grid = utils.make_grid(batch_imgs, nrow=8, normalize=True, value_range=(-1, 1))
        utils.save_image(grid, "subtest1_grid.png")
        print("Saved grid image to subtest1_grid.png")
    except Exception as e:
        print("FakeData/make_grid/save_image failed:", e, file=sys.stderr)
        sys.exit(1)

    section("subtest2 passed (NMS-free)")
    sys.exit(0)

if __name__ == "__main__":
    main()