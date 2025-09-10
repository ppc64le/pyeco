## ✅ Program : LightGBM Iris Mini Pipeline

### Purpose:
Trains a LightGBM model on a small Iris-like dataset and generates predictions, visuals, and metadata.

### Packages Used:
lightgbm pyarrow pillow scikit-learn

### Functionality:
Splits a minimal dataset into train/test sets.
Trains a multiclass LightGBM model.
Predicts test labels and calculates accuracy.
Uses pyarrow to save test data with predictions as .parquet.
Generates a feature importance image with Pillow.
Saves model metadata as .json and the model as .txt.
