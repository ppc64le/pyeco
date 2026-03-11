# mpl-example.py
# Self-contained sanity example (Matplotlib + ImageIO + Pillow), independent test.

import os
import sys
import time
import numpy as np
import imageio.v2 as imageio

# Headless backend for servers/CI
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULT = {"ok": 0, "warn": 0, "fail": 0, "checks": 0}

def log_ok(msg):
    print(f"[OK] {msg}"); RESULT["ok"] += 1; RESULT["checks"] += 1

def log_warn(msg):
    print(f"[warn] {msg}"); RESULT["warn"] += 1; RESULT["checks"] += 1

def log_fail(msg):
    print(f"[fail] {msg}"); RESULT["fail"] += 1; RESULT["checks"] += 1

def _ensure_rgb_for_jpeg(arr):
    # Converts RGBA/LA/Gray -> RGB for JPEG compatibility
    if arr.ndim == 3 and arr.shape[2] == 4:
        print("[info] Detected RGBA -> dropping alpha for JPEG.")
        return arr[:, :, :3]
    if arr.ndim == 2:
        print("[info] Detected grayscale -> stacking to RGB for JPEG.")
        return np.stack([arr, arr, arr], axis=-1)
    if arr.ndim == 3 and arr.shape[2] == 1:
        print("[info] Detected single-channel -> repeating to RGB for JPEG.")
        return np.repeat(arr, 3, axis=2)
    return arr

def main():
    print("\n=== [mpl-example] Start ===")
    t0 = time.time()
    try:
        # Prepare data
        x = np.linspace(0, 2*np.pi, 600, dtype=np.float64)
        y = np.sin(x) * np.exp(-0.08 * x)
        print(f"[info] Data prepared: x.shape={x.shape}, y.shape={y.shape}")

        # Plot
        fig, ax = plt.subplots(figsize=(6.5, 4.0), dpi=120)
        ax.plot(x, y, color="royalblue", linewidth=2, label="sin(x)*exp(-0.08x)")
        ax.set_title("Matplotlib + ImageIO Example")
        ax.set_xlabel("x"); ax.set_ylabel("y"); ax.grid(True); ax.legend()
        fig.tight_layout()

        # Save PNG
        png_path = "ex_plot.png"
        fig.savefig(png_path)  # PNG may carry alpha depending on backend/theme
        plt.close(fig)
        log_ok(f"PNG written: {png_path} | size={os.path.getsize(png_path)} bytes")

        # Read PNG → write JPEG (safe RGB)
        arr = imageio.imread(png_path)
        print(f"[info] Loaded PNG via ImageIO: shape={arr.shape}, dtype={arr.dtype}")
        if float(arr.std()) == 0.0:
            log_fail("PNG appears uniform (unexpected).")
        else:
            log_ok("PNG is non-uniform (expected).")

        jpg_path = "ex_plot.jpg"
        imageio.imwrite(jpg_path, _ensure_rgb_for_jpeg(arr), quality=92)
        log_ok(f"JPEG written: {jpg_path} | size={os.path.getsize(jpg_path)} bytes")

        jpg = imageio.imread(jpg_path)
        if jpg.ndim != 3 or jpg.shape[2] != 3:
            log_fail("JPEG is not RGB.")
        else:
            log_ok("JPEG is RGB as expected.")
    except Exception as e:
        log_fail(f"Unhandled exception: {e}")

    dt = time.time() - t0
    status = "PASS" if RESULT["fail"] == 0 else "FAIL"
    print(f"[RESULT] {status} | checks={RESULT['checks']}, ok={RESULT['ok']}, "
          f"warns={RESULT['warn']}, fails={RESULT['fail']}, time={dt:.2f}s")
    print("=== [mpl-example] End ===")
    sys.exit(1 if RESULT["fail"] else 0)

if __name__ == "__main__":
    main()
