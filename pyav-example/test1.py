import io
import numpy as np
from PIL import Image, ImageFilter
import av
import ml_dtypes
import llvmlite.binding as llvm
import ctypes

def test_full_stack_rawvideo():
    print("🎯 Starting full-stack test (rawvideo fallback)")

    # 1. Pillow image creation
    image = Image.new("L", (64, 64), color=100)
    image = image.filter(ImageFilter.CONTOUR)
    img_np = np.array(image, dtype=np.float32)

    # 2. LLVM brightness adjustment (via JIT)
    llvm.initialize(); llvm.initialize_native_target(); llvm.initialize_native_asmprinter()
    brightness_ir = """
    define float @adjust(float %pixel, float %factor) {
    entry:
      %scaled = fmul float %pixel, %factor
      ret float %scaled
    }
    """
    mod = llvm.parse_assembly(brightness_ir); mod.verify()
    target = llvm.Target.from_default_triple()
    tm = target.create_target_machine()
    engine = llvm.create_mcjit_compiler(llvm.parse_assembly(""), tm)
    engine.add_module(mod); engine.finalize_object()
    ptr = engine.get_function_address("adjust")
    adjust_fn = ctypes.CFUNCTYPE(ctypes.c_float, ctypes.c_float, ctypes.c_float)(ptr)
    adjusted_np = np.vectorize(lambda px: adjust_fn(px / 255.0, 1.5) * 255.0)(img_np).astype(np.uint8)

    # 3. ml_dtypes usage
    img_float8 = (adjusted_np / 255.0).astype(ml_dtypes.float8_e5m2)
    assert img_float8.shape == (64, 64)

    # 4. Encode using rawvideo
    frame_rgb = np.stack([adjusted_np]*3, axis=-1)
    frame = av.VideoFrame.from_ndarray(frame_rgb, format='rgb24')

    output = io.BytesIO()
    container = av.open(output, mode='w', format='avi')
    stream = container.add_stream('rawvideo', rate=25)
    stream.width = frame.width
    stream.height = frame.height
    stream.pix_fmt = 'rgb24'

    for packet in stream.encode(frame):
        container.mux(packet)
    container.close()

    video_bytes = output.getvalue()
    assert len(video_bytes) > 0, "Raw video is empty!"

    print("✅ Rawvideo fallback test passed – full-stack integration works without re-encoding!")

if __name__ == "__main__":
    test_full_stack_rawvideo()
