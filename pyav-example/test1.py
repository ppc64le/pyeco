import av

print("=== Test 1: Video File Analysis ===")
try:
    print("Skipping video analysis test as no video file is present.")
    print("[INFO] If a video file named 'input.mp4' were present, it would analyze its properties here.")
    # You can add a placeholder to demonstrate the import is working
    print(f"[INFO] Av package version: {av.__version__}")
except Exception as e:
    print(f"[ERROR] An error occurred during the 'av' import test: {e}")
print("=== Sub-Test 1 Complete ===")
