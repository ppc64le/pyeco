# sub-test1.py
# Independent test: generates its own outputs and validates them (no shared files).

import os
import sys
import time
import numpy as np
import imageio.v2 as imageio

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULT = {"ok": 0, "warn": 0, "fail": 0, "checks": 0}

def log_ok(msg): print(f"[OK] {msg}"); RESULT["ok"] += 1; RESULT["checks"] += 1
def log_warn(msg): print(f"[warn] {msg}"); RESULT["warn"] += 1; RESULT["checks"] += 1
def log_fail(msg): print(f"[fail] {msg}"); RESULT["fail"] += 1; RESULT["checks"] += 1

def _ensure_rgb_for_jpeg(arr):
    if arr.ndim == 3 and arr.shape[2] == 4:
        print("[info] RGBA detected -> dropping alpha for JPEG.")
        return arr[:, :, :3]
    if arr.ndim == 2:
        print("[info] Grayscale -> stacking to RGB for JPEG.")
        return np.stack([arr, arr, arr], axis=-1)
    return arr

def _check_nonuniform(arr, name):
    s = float(arr.std())
    print(f"[info] {name} std={s:.4f}")
    if s == 0.0: log_fail(f"{name} appears uniform.")
    else: log_ok(f"{name} looks non-uniform.")

def run_static():
    print("\n=== [sub-test1] Static PNG/JPEG ===")
    t0 = time.time()
    try:
        t = np.linspace(0, 1, 700, dtype=np.float64)
        y = np.cos(10*np.pi*t) * np.exp(-3*t)
        print(f"[info] Data: t.shape={t.shape}, y.min={y.min():.3f}, y.max={y.max():.3f}")

        fig, ax = plt.subplots(figsize=(7, 4), dpi=120)
        ax.plot(t, y, color="steelblue", linewidth=2)
        ax.set_title("Damped Cosine (sub-test1)")
        ax.set_xlabel("t"); ax.set_ylabel("y"); ax.grid(True)
        fig.tight_layout()

        png_path = "st1_static.png"
        fig.savefig(png_path)
        plt.close(fig)
        log_ok(f"PNG written: {png_path} | size={os.path.getsize(png_path)} bytes")

        arr = imageio.imread(png_path)
        _check_nonuniform(arr, "st1 PNG")

        jpg_path = "st1_static.jpg"
        imageio.imwrite(jpg_path, _ensure_rgb_for_jpeg(arr), quality=92)
        log_ok(f"JPEG written: {jpg_path} | size={os.path.getsize(jpg_path)} bytes")

        jpg = imageio.imread(jpg_path)
        if jpg.ndim != 3 or jpg.shape[2] != 3:
            log_fail("st1 JPEG not RGB.")
        else:
            log_ok("st1 JPEG is RGB.")
            _check_nonuniform(jpg, "st1 JPEG")
    except Exception as e:
        log_fail(f"Static section error: {e}")
    print(f"[done] Static completed in {time.time()-t0:.2f}s")

def run_gif(n_frames=24, width=640, height=360):
    print("\n=== [sub-test1] Animated GIF ===")
    t0 = time.time()
    try:
        xs = np.linspace(0, 2*np.pi, 400, dtype=np.float64)
        frames = []
        print(f"[info] GIF config: frames={n_frames}, canvas={width}x{height}")

        for i in range(n_frames):
            phase = i * (2*np.pi / n_frames)
            ys = np.sin(xs + phase)

            fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
            ax.plot(xs, ys, color="teal", linewidth=2)
            ax.set_ylim(-1.2, 1.2)
            ax.set_title(f"sub-test1 GIF frame {i+1}/{n_frames}")
            ax.set_xlabel("x"); ax.set_ylabel("sin(x+phase)"); ax.grid(True)
            fig.tight_layout()
            fig.canvas.draw()

            buf = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8)
            buf = buf.reshape((height, width, 4))
            rgba = buf[:, :, [1, 2, 3, 0]]  # ARGB -> RGBA
            frames.append(rgba)
            plt.close(fig)

            if (i + 1) % max(1, n_frames // 4) == 0:
                print(f"[info] Rendered {i+1}/{n_frames} frames")

        gif_path = "st1_wave.gif"
        imageio.mimsave(gif_path, frames, duration=0.06)
        log_ok(f"GIF written: {gif_path} | frames={len(frames)} | size={os.path.getsize(gif_path)} bytes")

        # Validate motion quickly
        if len(frames) < 2:
            log_fail("GIF has fewer than 2 frames.")
        else:
            f0, f1 = frames[0], frames[1]
            mad = float(np.mean(np.abs(f1.astype(np.float32) - f0.astype(np.float32))))
            print(f"[info] Frame diff (0->1) MAD={mad:.2f}")
            if mad == 0.0:
                log_fail("GIF frames look identical (no motion).")
            else:
                log_ok("GIF motion detected.")
    except Exception as e:
        log_fail(f"GIF section error: {e}")
    print(f"[done] GIF completed in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    t_all = time.time()
    run_static()
    run_gif()
    dt = time.time() - t_all
    status = "PASS" if RESULT["fail"] == 0 else "FAIL"
    print(f"[RESULT] {status} | checks={RESULT['checks']}, ok={RESULT['ok']}, "
          f"warns={RESULT['warn']}, fails={RESULT['fail']}, time={dt:.2f}s")
    sys.exit(1 if RESULT["fail"] else 0)
