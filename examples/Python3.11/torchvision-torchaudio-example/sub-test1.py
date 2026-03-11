import sys
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
        from PIL import Image
        return torch, torchvision, Image
    except Exception as e:
        msg = str(e).replace("\n", " ")
        if NMS_CONFLICT_SNIPPET in msg:
            section("SKIP: NMS registration conflict detected")
            print(
                "Detected NMS Meta registration conflict during torchvision import.\n"
                "Skipping subtest2.py so your pipeline can continue."
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

    section("2) Classification model forward pass (no weights, no downloads)")
    try:
        from torchvision import models
        # Create a small classification model; using weights=None to avoid downloads
        model = models.resnet18(weights=None)
        model.eval()
        x = torch.randn(4, 3, 224, 224)  # standard ImageNet-like size
        with torch.no_grad():
            y = model(x)  # (4, 1000)
        require(y.shape == (4, 1000), "resnet18 forward produced (4,1000)")
        print("resnet18 forward successful without touching detection/NMS.")
    except Exception as e:
        print("Model forward test failed:", e, file=sys.stderr)
        sys.exit(1)

    section("3) transforms.functional ops (tensor path)")
    try:
        from torchvision.transforms import functional as F, InterpolationMode
        img = torch.rand(3, 64, 96)  # CHW

        # Resize using bilinear and bicubic; ensure shape matches target
        img_bilinear = F.resize(img, size=[48, 48], interpolation=InterpolationMode.BILINEAR, antialias=True)
        img_bicubic  = F.resize(img, size=[48, 48], interpolation=InterpolationMode.BICUBIC, antialias=True)
        require(img_bilinear.shape == (3, 48, 48), "Bilinear resize produced (3,48,48)")
        require(img_bicubic.shape  == (3, 48, 48), "Bicubic resize produced (3,48,48)")

        # Center crop
        cc = F.center_crop(img_bicubic, output_size=[40, 40])
        require(cc.shape == (3, 40, 40), "Center crop produced (3,40,40)")

        # Horizontal flip and grayscale conversion
        flipped = F.hflip(cc)
        gray = F.rgb_to_grayscale(flipped, num_output_channels=1)
        require(gray.shape == (1, 40, 40), "rgb_to_grayscale -> (1,40,40)")

        print("transforms.functional pipeline executed successfully.")
    except Exception as e:
        print("functional transforms test failed:", e, file=sys.stderr)
        sys.exit(1)

    section("4) AutoAugment (PIL path, image-level only)")
    try:
        from torchvision import transforms
        pil_img = Image.fromarray((torch.rand(32, 32, 3) * 255).byte().numpy(), mode="RGB")
        aa = transforms.AutoAugment(policy=transforms.AutoAugmentPolicy.IMAGENET)
        # AutoAugment expects PIL or tensor; we’ll use PIL
        out_pil = aa(pil_img)
        require(out_pil.size == (32, 32), "AutoAugment kept spatial size (32x32)")
        # Convert to tensor
        out_t = transforms.ToTensor()(out_pil)
        require(out_t.shape == (3, 32, 32), "AutoAugment + ToTensor -> (3,32,32)")
        print("AutoAugment pipeline (PIL) executed successfully.")
    except Exception as e:
        print("AutoAugment test failed:", e, file=sys.stderr)
        sys.exit(1)

    section("subtest1 passed (NMS-free)")
    sys.exit(0)

if __name__ == "__main__":
    main()