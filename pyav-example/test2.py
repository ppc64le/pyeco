import av

print("=== Core Library Attribute Test ===")
try:
    # Test for a core, non-changing attribute
    if av.time_base is not None:
        print(f"[INFO] The 'av.time_base' attribute exists and is: {av.time_base}")
        print("[INFO] This confirms the core library is functional.")
    else:
        print("[ERROR] The 'av.time_base' attribute could not be accessed.")
except Exception as e:
    print(f"[ERROR] Core library attribute test failed: {e}")

print("=== Test Complete ===")
