import os
import sys
import time
import math
import numpy as np
import imageio.v2 as imageio
from PIL import Image, PngImagePlugin

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULT = {"ok": 0, "warn": 0, "fail": 0, "checks": 0}
def log_ok(msg): print(f"[OK] {msg}"); RESULT["ok"] += 1; RESULT["checks"] += 1
def log_warn(msg): print(f"[warn] {msg}"); RESULT["warn"] += 1; RESULT["checks"] += 1
def log_fail(msg): print(f"[fail] {msg}"); RESULT["fail"] += 1; RESULT["checks"] += 1

def _ensure_rgb(arr):
    if arr.ndim == 3 and arr.shape[2] == 4:
        return arr[:, :, :3]
    if arr.ndim == 2:
        return np.stack([arr, arr, arr], axis=-1)
    if arr.ndim == 3 and arr.shape[2] == 1:
        return np.repeat(arr, 3, axis=2)
    return arr

def test_dpi_and_size(out_png="st3_dpi.png", fig_size=(5.2, 3.1), dpi=137):
    print("\n=== [sub-test3] DPI & pixel size validation ===")
    t0 = time.time()
    try:
        fig, ax = plt.subplots(figsize=fig_size, dpi=dpi)
        x = np.linspace(0, 2*np.pi, 400)
        ax.plot(x, np.sin(x), color="crimson")
        ax.set_title(f"DPI test ({dpi})")
        ax.grid(True)
        fig.tight_layout()
        fig.savefig(out_png)
        plt.close(fig)

        pix_expected = (int(round(fig_size[0] * dpi)), int(round(fig_size[1] * dpi)))
        # Read back to confirm pixel dimensions
        img = Image.open(out_png)
        pix_actual = img.size  # (W, H)
        log_ok(f"DPI PNG written: {out_png} | size={os.path.getsize(out_png)} bytes")
        print(f"[info] Expected pixels={pix_expected}, Actual pixels={pix_actual}")
        if pix_actual != pix_expected:
            log_warn(f"Pixel size mismatch expected={pix_expected} vs actual={pix_actual} (may differ due to bbox_inches/tight_layout).")
        else:
            log_ok("Pixel size matches figsize*dpi.")
    except Exception as e:
        log_fail(f"DPI check error: {e}")
    print(f"[done] DPI check completed in {time.time()-t0:.2f}s")

def test_alpha_and_jpeg(out_png="st3_alpha.png", out_jpg="st3_alpha.jpg"):
    print("\n=== [sub-test3] Alpha overlay & safe JPEG ===")
    t0 = time.time()
    try:
        # Base gradient (RGB)
        H, W = 240, 360
        x = np.linspace(0, 255, W, dtype=np.uint8)
        grad = np.tile(x, (H, 1))
        rgb = np.dstack([grad, grad[:, ::-1], np.full_like(grad, 128)])

        # Create a semi-transparent overlay circle
        Y, X = np.ogrid[:H, :W]
        cy, cx, r = H//2, W//2, min(H, W)//3
        mask = ((Y - cy)**2 + (X - cx)**2) <= (r**2)
        alpha = np.zeros((H, W), dtype=np.uint8)
        alpha[mask] = 160  # semi-transparent
        rgba = np.dstack([rgb, alpha])

        # Save RGBA PNG via ImageIO
        imageio.imwrite(out_png, rgba)
        log_ok(f"RGBA PNG written: {out_png} | size={os.path.getsize(out_png)} bytes")

        # Read RGBA, convert to RGB for JPEG
        arr = imageio.imread(out_png)
        if arr.shape[2] != 4:
            log_warn("PNG did not load as RGBA (unexpected), continuing.")
        rgb_safe = _ensure_rgb(arr)
        imageio.imwrite(out_jpg, rgb_safe, quality=92)
        log_ok(f"JPEG written: {out_jpg} | size={os.path.getsize(out_jpg)} bytes")

        # Quick sanity: non-uniformity and RGB channels
        if float(rgb_safe.std()) == 0.0: log_fail("RGB-safe array appears uniform.")
        else: log_ok("RGB-safe array non-uniform.")
        jpg = imageio.imread(out_jpg)
        if jpg.ndim != 3 or jpg.shape[2] != 3:
            log_fail("Alpha->JPEG result is not RGB.")
        else:
            log_ok("Alpha->JPEG is RGB.")
    except Exception as e:
        log_fail(f"Alpha/JPEG error: {e}")
    print(f"[done] Alpha/JPEG completed in {time.time()-t0:.2f}s")

def test_png_metadata(path="st3_meta.png"):
    print("\n=== [sub-test3] PNG text metadata ===")
    t0 = time.time()
    try:
        # Simple RGB image
        H, W = 100, 140
        img = Image.new("RGB", (W, H), (10, 20, 30))
        meta = PngImagePlugin.PngInfo()
        meta.add_text("Author", "Sai Kiran (test)")
        meta.add_text("Description", "PNG metadata demo")
        img.save(path, pnginfo=meta)
        log_ok(f"Metadata PNG written: {path} | size={os.path.getsize(path)} bytes")

        # Read back metadata
        im2 = Image.open(path)
        txt = getattr(im2, "text", {})
        print(f"[info] PNG text keys: {list(txt.keys())}")
        if "Author" in txt and "Description" in txt:
            log_ok("PNG text metadata keys present.")
        else:
            log_warn("PNG text metadata keys missing on readback (Pillow build may vary).")
    except Exception as e:
        log_fail(f"PNG metadata error: {e}")
    print(f"[done] Metadata test completed in {time.time()-t0:.2f}s")

def test_multi_dpi_batch():
    print("\n=== [sub-test3] Small multi-DPI batch ===")
    t0 = time.time()
    try:
        dpis = [72, 100, 200]
        for d in dpis:
            fig, ax = plt.subplots(figsize=(3.0, 2.0), dpi=d)
            t = np.linspace(0, 1, 200)
            ax.plot(t, np.sin(8*np.pi*t), color="royalblue")
            ax.set_title(f"DPI {d}")
            ax.set_axis_off()
            fig.tight_layout(pad=0)
            out = f"st3_batch_dpi{d}.png"
            fig.savefig(out)
            plt.close(fig)
            log_ok(f"Batch PNG written: {out} | size={os.path.getsize(out)} bytes")
    except Exception as e:
        log_fail(f"Multi-DPI batch error: {e}")
    print(f"[done] Multi-DPI batch completed in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    t_all = time.time()
    test_dpi_and_size()
    test_alpha_and_jpeg()
    test_png_metadata()
    test_multi_dpi_batch()
    dt = time.time() - t_all
    status = "PASS" if RESULT["fail"] == 0 else "FAIL"
    print(f"[RESULT] {status} | checks={RESULT['checks']}, ok={RESULT['ok']}, "
          f"warns={RESULT['warn']}, fails={RESULT['fail']}, time={dt:.2f}s")
    sys.exit(1 if RESULT["fail"] else 0)
