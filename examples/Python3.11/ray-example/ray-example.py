import ray
import joblib
import numpy as np
from ray.util.joblib import register_ray
from sklearn.datasets import load_digits
from sklearn.model_selection import RandomizedSearchCV
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

print("✅ Starting deep Ray integration test")

ray.init()
register_ray()

# --------------------------------------------------
# Step 1: Load and preprocess data using NumPy
# --------------------------------------------------
digits = load_digits()
X = digits.data.astype(np.float32)
y = digits.target

# Normalize using NumPy (explicit heavy usage)
X = X / np.max(X)

assert X.shape[0] == y.shape[0]
print("📊 Dataset loaded and normalized")

# --------------------------------------------------
# Step 2: Ray remote preprocessing task
# --------------------------------------------------
@ray.remote
def batch_stats(batch):
    return {
        "mean": float(np.mean(batch)),
        "std": float(np.std(batch))
    }

batches = np.array_split(X, 4)
stat_refs = [batch_stats.remote(b) for b in batches]
stats = ray.get(stat_refs)

print("📈 Distributed batch statistics:", stats)

# --------------------------------------------------
# Step 3: Ray actor for tracking training progress
# --------------------------------------------------
@ray.remote
class TrainingTracker:
    def __init__(self):
        self.trials = 0

    def increment(self):
        self.trials += 1
        return self.trials

    def get(self):
        return self.trials

tracker = TrainingTracker.remote()

# --------------------------------------------------
# Step 4: Build sklearn pipeline
# --------------------------------------------------
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("svc", SVC(kernel="rbf"))
])

# ✅ FULL parameter space (now matches your reference)
param_space = {
    "svc__C": np.logspace(-6, 6, 30),
    "svc__gamma": np.logspace(-8, 8, 30),
    "svc__tol": np.logspace(-4, -1, 30),
    "svc__class_weight": [None, "balanced"],
}

search = RandomizedSearchCV(
    pipeline,
    param_space,
    cv=5,
    n_iter=300,
    verbose=10,
    n_jobs=-1,
)

# --------------------------------------------------
# Step 5: Train using Ray as Joblib backend
# --------------------------------------------------
with joblib.parallel_backend("ray"):
    search.fit(X, y)
    tracker.increment.remote()

# --------------------------------------------------
# Step 6: Validate results
# --------------------------------------------------
best_params = search.best_params_
trial_count = ray.get(tracker.get.remote())

print("✅ Best parameters found:", best_params)
print("🔢 Number of Ray-tracked training runs:", trial_count)

assert isinstance(best_params, dict)
assert trial_count == 1

print("🎉 Deep Ray integration example completed successfully")

ray.shutdown()
