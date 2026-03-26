## ✅ Program: Ray Distributed Computing and ML Hyperparameter Search Example

## Purpose: Demonstrates distributed computing using the Ray framework, including parallel task execution, actors, object store usage, and distributed scikit‑learn hyperparameter tuning with Joblib + Ray backend.

### Packages used:
ray numpy joblib scikit‑learn

### Functionality:

- Initializes a local Ray runtime.
- Loads and preprocesses the sklearn digits dataset using NumPy.
- Executes distributed preprocessing tasks using Ray remote functions.
- Uses Ray actors to track execution state.
- Builds a scikit‑learn pipeline with scaling and SVM classification.
- Performs large‑scale hyperparameter search using RandomizedSearchCV.
- Executes cross‑validation in parallel using Ray as a Joblib backend.
- Retrieves and validates the best model parameters.

### How to run the example :
```
chmod +x install_test_example.sh
./install_test_example.sh
```

### License:
It's covered under Apache 2.0 licenses
