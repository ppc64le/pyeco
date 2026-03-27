# sub-test3.py - Ray object store and task dependency test

import ray
import numpy as np

print("🚀 Starting Ray object-store sub-test")

ray.init()

@ray.remote
def compute_sum(arr):
    return int(np.sum(arr))

@ray.remote
def compute_mean(arr):
    return float(np.mean(arr))

# Create large NumPy data
data = np.random.randint(0, 100, size=(1000, 100)).astype(np.int32)

# Put data into Ray object store
data_ref = ray.put(data)

# Launch dependent tasks
sum_ref = compute_sum.remote(data_ref)
mean_ref = compute_mean.remote(data_ref)

sum_result, mean_result = ray.get([sum_ref, mean_ref])

print("Sum:", sum_result)
print("Mean:", mean_result)

# Validation
assert sum_result > 0
assert 0 <= mean_result <= 100

print("✅ Sub-test 3 passed: Ray object store and task dependencies work")

ray.shutdown()
