import paddle
import paddle.nn as nn
import numpy as np
import pandas as pd
from PIL import Image

print("✅ Sub-test 3: PaddlePaddle image-like tensor + Pandas + Pillow")

# --- Simulate a batch of grayscale 8x8 images ---
batch_size = 4
images_np = np.random.rand(batch_size, 1, 8, 8).astype(np.float32)
images_t  = paddle.to_tensor(images_np)
print("Image batch shape:", images_t.shape)

# --- Simple conv layer forward pass ---
conv = nn.Conv2D(in_channels=1, out_channels=4, kernel_size=3, padding=1)
feature_maps = conv(images_t)
print("Feature map shape:", feature_maps.shape)

# --- Flatten and collect stats into a DataFrame ---
flat = feature_maps.numpy().reshape(batch_size, -1)
df   = pd.DataFrame(flat, columns=[f"feat_{i}" for i in range(flat.shape[1])])
print("Feature DataFrame head:\n", df.head())
print("Column means:\n", df.mean())

# --- Pillow: save one feature map channel as an image ---
channel_0 = feature_maps[0, 0].numpy()
channel_0_norm = ((channel_0 - channel_0.min()) /
                  (channel_0.max() - channel_0.min() + 1e-8) * 255).astype(np.uint8)
img = Image.fromarray(channel_0_norm, mode='L')
img.save("feature_map.png")
print("Saved feature_map.png via Pillow")

import os
os.remove("feature_map.png")

print("✅ Sub-test 3 completed successfully.")
