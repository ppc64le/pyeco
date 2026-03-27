# sub-test2.py
# Ray actor coordination and state consistency test

import ray
import time

print("🚀 Starting expanded Ray actor sub-test")

ray.init()

@ray.remote
class JobCounter:
    def __init__(self):
        self.count = 0
        self.history = []

    def record(self, value):
        time.sleep(0.2)
        self.count += 1
        self.history.append(value)
        return self.count

    def summary(self):
        return {
            "total_jobs": self.count,
            "history": list(self.history)
        }

# Create actor
counter = JobCounter.remote()

# Launch multiple actor method calls
tasks = [
    counter.record.remote(i * 10)
    for i in range(6)
]

results = ray.get(tasks)

# Fetch final state
summary = ray.get(counter.summary.remote())

# Validation
assert results == [1, 2, 3, 4, 5, 6]
assert summary["total_jobs"] == 6
assert summary["history"] == [0, 10, 20, 30, 40, 50]

print("Actor update results:", results)
print("Actor summary:", summary)

print("✅ Sub-test 2 passed: Actor state consistency verified")

ray.shutdown()
