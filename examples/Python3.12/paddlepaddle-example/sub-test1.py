import paddle
import numpy as np

print("✅ Sub-test 1: PaddlePaddle basic tensor operations")

# Tensor creation
a = paddle.to_tensor([[1.0, 2.0], [3.0, 4.0]])
b = paddle.to_tensor([[5.0, 6.0], [7.0, 8.0]])

# Basic arithmetic
c = paddle.add(a, b)
d = paddle.matmul(a, b)
print("Add result:\n", c.numpy())
print("Matmul result:\n", d.numpy())

# Reduction ops
print("Sum:", paddle.sum(a).item())
print("Mean:", paddle.mean(a).item())

# NumPy interop
np_arr = np.array([1.0, 2.0, 3.0], dtype=np.float32)
tensor_from_np = paddle.to_tensor(np_arr)
back_to_np     = tensor_from_np.numpy()
print("NumPy → Tensor → NumPy:", back_to_np)

print(f"PaddlePaddle version: {paddle.__version__}")
print("✅ Sub-test 1 completed successfully.")
