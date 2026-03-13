# sub-test2.py
# Independent test: produces its own outputs (no reliance on other tests).

import os
import sys
import math
import time
import numpy as np
import imageio.v2 as imageio
from PIL import Image

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULT = {"ok": 0, "warn": 0, "fail": 0, "checks": 0}
def log_ok(msg): print(f"[OK] {msg}"); RESULT["ok"] += 1; RESULT["checks"] += 1
def log_warn(msg): print(f"[warn] {msg}"); RESULT["warn"] += 1; RESULT["checks"] += 1
def log_fail(msg): print(f"[fail] {msg}"); RESULT["fail"] += 1; RESULT["checks"] += 1

def _check_nonuniform(arr, name):
    s = float(arr.std())
    print(f"[info] {name} std={s:.4f}")
    if s == 0.0: log_fail(f"{name} appears uniform.")
    else: log_ok(f"{name} looks non-uniform.")

def gen_contour_png(out="st2_contour.png"):
    print("\n=== [sub-test2] Contour ===")
    t0 = time.time()
    try:
        x = np.linspace(-4, 4, 480)
        y = np.linspace(-3, 3, 360)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X) * np.cos(Y) + 0.1 * (X - Y)
        print(f"[info] Grid: X={X.shape}, Y={Y.shape}, Z.min={Z.min():.3f}, Z.max={Z.max():.3f}")

        fig, ax = plt.subplots(figsize=(7, 4.5), dpi=150)
        cs = ax.contour(X, Y, Z, levels=np.linspace(Z.min(), Z.max(), 12),
                        colors="black", linewidths=0.7, antialiased=True)
        cf = ax.contourf(X, Y, Z, levels=24, cmap="viridis", antialiased=True)
        ax.clabel(cs, inline=True, fontsize=7, fmt="%.2f")
        ax.set_title("Contour/Contourf (sub-test2)")
        ax.set_xlabel("x"); ax.set_ylabel("y")
        fig.colorbar(cf, ax=ax, shrink=0.9, label="f(x,y)")
        fig.tight_layout()
        fig.savefig(out, bbox_inches="tight")
        plt.close(fig)

        log_ok(f"PNG written: {out} | size={os.path.getsize(out)} bytes")
        arr = imageio.imread(out)
        _check_nonuniform(arr, "st2 contour")
    except Exception as e:
        log_fail(f"Contour section error: {e}")
    print(f"[done] Contour completed in {time.time()-t0:.2f}s")

def gen_tiled_large_png(H=1800, W=2400, out_png="st2_tiled.png", thumb_jpg="st2_tiled_thumb.jpg"):
    print("\n=== [sub-test2] Tiled large heatmap ===")
    t0 = time.time()
    try:
        # Synthetic field
        y = np.linspace(-3.5, 3.5, H, dtype=np.float32)
        x = np.linspace(-5.0, 5.0, W, dtype=np.float32)
        X, Y = np.meshgrid(x, y, indexing="xy")
        Z = np.sinc(np.sqrt(X**2 + Y**2)) * np.cos(2*X) * np.sin(2*Y)
        print(f"[info] Field: Z.shape={Z.shape}, Z.min={Z.min():.4f}, Z.max={Z.max():.4f}")

        # Tiling
        tile_h, tile_w = 360, 400
        nty, ntx = math.ceil(H/tile_h), math.ceil(W/tile_w)
        vmin, vmax = float(Z.min()), float(Z.max())
        print(f"[info] Tiling plan: {nty}x{ntx}, tile ~{tile_h}x{tile_w}, vmin={vmin:.4f}, vmax={vmax:.4f}")

        def _draw_tile(z, th, tw):
            fig, ax = plt.subplots(figsize=(tw/100, th/100), dpi=100)
            ax.imshow(z, cmap="magma", vmin=vmin, vmax=vmax, origin="lower", interpolation="nearest")
            ax.set_axis_off()
            fig.tight_layout(pad=0)
            fig.canvas.draw()
            buf = fig.canvas.tostring_argb()
            arr = np.frombuffer(buf, dtype=np.uint8).reshape(th, tw, 4)
            rgba = arr[:, :, [1, 2, 3, 0]]  # ARGB -> RGBA
            plt.close(fig)
            return Image.fromarray(rgba, mode="RGBA")

        canvas = Image.new("RGBA", (W, H))
        for ty in range(nty):
            row_t0 = time.time()
            for tx in range(ntx):
                y0, x0 = ty * tile_h, tx * tile_w
                tile = Z[y0:y0+tile_h, x0:x0+tile_w]
                img = _draw_tile(tile, tile.shape[0], tile.shape[1])
                canvas.paste(img, (x0, y0))
            print(f"[info] Tiled row {ty+1}/{nty} in {time.time()-row_t0:.2f}s")

        canvas.save(out_png)
        log_ok(f"Tiled PNG written: {out_png} | size={os.path.getsize(out_png)} bytes")

        # Thumbnail to exercise alpha->RGB
        thumb = canvas.resize((W//6, H//6), resample=Image.BILINEAR)
        rgb_bg = Image.new("RGB", thumb.size, (255, 255, 255))
        rgb_bg.paste(thumb, mask=thumb.split()[3])
        rgb_bg.save(thumb_jpg, quality=88)
        log_ok(f"Thumbnail JPEG written: {thumb_jpg} | size={os.path.getsize(thumb_jpg)} bytes")

        arr_png = imageio.imread(out_png)
        _check_nonuniform(arr_png, "st2 tiled PNG")
        jpg = imageio.imread(thumb_jpg)
        if jpg.ndim != 3 or jpg.shape[2] != 3:
            log_fail("st2 thumbnail JPEG is not RGB.")
        else:
            log_ok("st2 thumbnail JPEG is RGB.")
            _check_nonuniform(jpg, "st2 thumbnail JPEG")
    except Exception as e:
        log_fail(f"Tiled section error: {e}")
    print(f"[done] Tiled heatmap completed in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    t_all = time.time()
    gen_contour_png()
    gen_tiled_large_png()
    dt = time.time() - t_all
    status = "PASS" if RESULT["fail"] == 0 else "FAIL"
    print(f"[RESULT] {status} | checks={RESULT['checks']}, ok={RESULT['ok']}, "
          f"warns={RESULT['warn']}, fails={RESULT['fail']}, time={dt:.2f}s")
    sys.exit(1 if RESULT["fail"] else 0)
