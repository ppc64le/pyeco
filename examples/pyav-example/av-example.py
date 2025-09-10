# example.py - Integration test for av, ml_dtypes, llvmlite, Pillow
import io
import numpy as np
from PIL import Image
import av
import ml_dtypes
import llvmlite.binding as llvm

print("✅ Starting environment integration test...")

# ----------------------------------------
# 1. Create image using Pillow
# ----------------------------------------
print("🖼️ Creating image with Pillow...")
image = Image.new("RGB", (64, 64), color="green")
buffer = io.BytesIO()
image.save(buffer, format="PNG")
buffer.seek(0)
print("✅ Pillow image created and saved to memory.")

# ----------------------------------------
# 2. Use ml_dtypes to create an array
# ----------------------------------------
print("🔬 Creating array using ml_dtypes...")
arr = np.array([0.5, 1.5, 2.5, 3.5], dtype=ml_dtypes.float8_e5m2)
print("Array with ml_dtypes.float8_e5m2:", arr)
print("✅ ml_dtypes array created.")

# ----------------------------------------
# 3. Use AV to encode a frame made from NumPy
# ----------------------------------------
print("🎥 Encoding video frame using PyAV...")

# Convert image to NumPy and pass to AV
image_np = np.array(image)
frame = av.VideoFrame.from_ndarray(image_np, format="rgb24")

# Encode frame to in-memory video using rawvideo codec in AVI container
output = io.BytesIO()
container = av.open(output, mode='w', format='avi')  # AVI container
stream = container.add_stream('rawvideo', rate=24)  # rawvideo codec (no encoder dependency)
stream.width = frame.width
stream.height = frame.height
stream.pix_fmt = 'rgb24'

# Encode and mux all packets
for packet in stream.encode(frame):
    container.mux(packet)
container.close()
print("✅ PyAV video encoded in memory with rawvideo.")

# ----------------------------------------
# 4. Use llvmlite to run a simple LLVM IR (optional but meaningful)
# ----------------------------------------
print("⚙️ Running minimal LLVM IR with llvmlite...")

llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

llvm_ir = """
define i32 @add(i32 %a, i32 %b) {
entry:
  %sum = add i32 %a, %b
  ret i32 %sum
}
"""

mod = llvm.parse_assembly(llvm_ir)
mod.verify()
print("✅ LLVM IR parsed and verified.")

# ----------------------------------------
print("\n🎉 All packages tested successfully together!")
