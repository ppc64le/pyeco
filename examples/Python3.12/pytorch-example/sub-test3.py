import numpy as np
import torch

# Create a NumPy array
np_array = np.array([1, 2, 3, 4, 5])
print("NumPy array:", np_array)

# Convert NumPy array to PyTorch tensor
torch_tensor = torch.from_numpy(np_array)
print("Torch tensor:", torch_tensor)

# Perform a simple operation (e.g., multiply by 2)
torch_tensor = torch_tensor * 2
print("Torch tensor after multiplication:", torch_tensor)

# Convert back to NumPy array
np_array_back = torch_tensor.numpy()
print("NumPy array after conversion back:", np_array_back)
