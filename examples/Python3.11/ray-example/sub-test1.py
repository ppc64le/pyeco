# sub-test1.py
# Ray parallel computation and validation test

import ray
import numpy as np
import time

print("🚀 Starting expanded Ray parallel computation sub-test")

ray.init()

@ray.remote
def normalize_and_scale(chunk, scale):
    time.sleep(0.5)  # simulate CPU work
    chunk = chunk.astype(np.float32)
    normalized = chunk / np.max(chunk)
    return normalized * scale

# Create synthetic dataset
data = np.random.randint(1, 1000, size=(2000, 32))
scale_factor = 2.5

# Split data into batches
chunks = np.array_split(data, 4)

# Launch parallel Ray tasks
refs = [
    normalize_and_scale.remote(chunk, scale_factor)
    for chunk in chunks
]

results = ray.get(refs)

# Merge results
processed_data = np.vstack(results)

# Validation
assert processed_data.shape == data.shape
assert np.all(processed_data >= 0.0)
assert np.max(processed_data) <= scale_factor + 1e-5

print("✅ Parallel processing completed")
print("Processed data shape:", processed_data.shape)

# Extra sanity check
sample_mean = float(np.mean(processed_data))
print("Sample mean value:", sample_mean)
assert sample_mean > 0

print("🎉 Sub-test 1 passed: Parallel Ray tasks executed correctly")

ray.shutdown()
