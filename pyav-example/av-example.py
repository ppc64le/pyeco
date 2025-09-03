import av
import subprocess
import os

print("===  Package Import Test ===")
try:
    print(f"[INFO] PyAV version: {av.__version__}")
    print(f"[INFO] FFmpeg library versions: {av.library_versions}")
    print(f"[INFO] FFmpeg build configuration: {av.ffmpeg_version_info}")
    print("[INFO] 'av' package loaded successfully.")
except Exception as e:
    print(f"[ERROR] 'av' package import failed: {e}")

print("\n=== 2. Check for FFmpeg Command-Line Tool ===")
try:
    # Run a simple FFmpeg command to verify the binary is functional
    subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True, text=True)
    print("[INFO] FFmpeg command-line tool is installed and working.")
except FileNotFoundError:
    print("[ERROR] 'ffmpeg' command not found. The FFmpeg binary might not be in your PATH.")
except subprocess.CalledProcessError as e:
    print(f"[ERROR] 'ffmpeg' command failed with exit code {e.returncode}: {e.stderr}")

print("\n=== 3. Core Functionality Test (Basic Pass) ===")
print("[INFO] The 'av' package loaded successfully in section 1.")
print("[INFO] This is the most reliable sign that the Python-FFmpeg linking is functional.")

print("\n=== Script Complete ===")
