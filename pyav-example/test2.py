import io
import numpy as np
from PIL import Image
import av
import ml_dtypes
import llvmlite.binding as llvm

def test_image_processing_and_encoding():
    print("🚀 Starting secondary integration test...")

    # ----------------------------------------
    # 1. Create a gradient grayscale image with Pillow
    # ----------------------------------------
    print("🖼️ Creating gradient grayscale image...")
    width, height = 128, 64
    gradient = np.tile(np.linspace(0, 255, width, dtype=np.uint8), (height, 1))
    image = Image.fromarray(gradient, mode="L")
    print("✅ Grayscale image created.")

    # ----------------------------------------
    # 2. Use ml_dtypes for a small float8 conversion
    # ----------------------------------------
    print("🔬 Creating float8 array with ml_dtypes...")
    arr = np.array([0.1, 0.2, 0.3, 0.4], dtype=ml_dtypes.float8_e5m2)
    print("Array with ml_dtypes.float8_e5m2:", arr)
    print("✅ ml_dtypes array created.")

    # ----------------------------------------
    # 3. Use llvmlite to compile and run a multiply function
    # ----------------------------------------
    print("⚙️ Compiling multiply function with llvmlite...")

    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    llvm_ir = """
    define i32 @mul(i32 %a, i32 %b) {
    entry:
      %result = mul i32 %a, %b
      ret i32 %result
    }
    """

    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    with llvm.create_mcjit_compiler(mod, target_machine) as ee:
        ee.finalize_object()
        func_ptr = ee.get_function_address("mul")
        import ctypes
        cfunc = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int)(func_ptr)
        result = cfunc(6, 7)
        assert result == 42
        print(f"✅ llvmlite multiply function works: 6 * 7 = {result}")

    # ----------------------------------------
    # 4. Use PyAV to encode the grayscale image as rawvideo AVI
    # ----------------------------------------
    print("🎥 Encoding grayscale image using PyAV...")

    image_np = np.array(image)
    frame = av.VideoFrame.from_ndarray(image_np, format="gray8")

    output = io.BytesIO()
    container = av.open(output, mode='w', format='avi')
    stream = container.add_stream('rawvideo', rate=30)
    stream.width = frame.width
    stream.height = frame.height
    stream.pix_fmt = 'gray8'

    for packet in stream.encode(frame):
        container.mux(packet)
    container.close()

    print("✅ PyAV video encoded in memory with rawvideo (grayscale).")
    print("\n🎉 Secondary integration test completed successfully!")

if __name__ == "__main__":
    test_image_processing_and_encoding()
