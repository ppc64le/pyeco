# subtest_pillow.py
from PIL import Image, ImageChops
import numpy as np
import io

def test_pillow_intermediate():
    print("🧪 Starting intermediate Pillow test...")

    # Step 1: Create RGB image with gradient
    width, height = 128, 128
    img = Image.new("RGB", (width, height))
    for x in range(width):
        for y in range(height):
            img.putpixel((x, y), (x % 256, y % 256, (x + y) % 256))
    print("🎨 Created image with RGB gradient")

    # Step 2: Convert to grayscale and validate mode
    gray_img = img.convert("L")
    assert gray_img.mode == "L", "Failed to convert to grayscale"
    print("🌗 Converted to grayscale successfully")

    # Step 3: Resize image down and then back up
    small = gray_img.resize((32, 32))
    restored = small.resize((width, height))
    assert restored.size == (128, 128), "Image resizing failed"
    print("🔁 Resized image down and back up")

    # Step 4: Crop center and paste into new canvas
    crop_box = (32, 32, 96, 96)
    cropped = gray_img.crop(crop_box)
    canvas = Image.new("L", (128, 128), color=0)
    canvas.paste(cropped, (16, 16))
    print("🖼️ Cropped and pasted onto canvas")

    # Step 5: Check pixel integrity
    np_original = np.array(gray_img)
    np_modified = np.array(canvas)
    diff = np.sum(np.abs(np_original - np_modified))
    assert diff > 0, "Unexpected: No pixel difference found"
    print("🔬 Verified pixel-level modifications")

    # Step 6: Save and reload from memory
    buffer = io.BytesIO()
    canvas.save(buffer, format="PNG")
    buffer.seek(0)
    reloaded = Image.open(buffer)
    assert reloaded.size == (128, 128), "Reloaded image size mismatch"
    print("💾 Saved to and reloaded from memory")

    print("✅ Intermediate Pillow test passed successfully!")


if __name__ == "__main__":
    test_pillow_intermediate()
