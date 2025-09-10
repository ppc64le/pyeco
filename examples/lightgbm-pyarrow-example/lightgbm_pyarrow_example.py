import lightgbm as lgb
import pyarrow as pa
import pyarrow.parquet as pq
from PIL import Image, ImageDraw
import json
import os
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

# Create output folder
os.makedirs("output", exist_ok=True)

# Load the real Iris dataset
iris = load_iris()
X = iris.data.astype(np.float32)
y = iris.target.astype(np.int32)
feature_names = iris.feature_names  # ['sepal length (cm)', 'sepal width (cm)', ...]

# Stratified train-test split (70% train, 30% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# LightGBM training
train_dataset = lgb.Dataset(X_train, label=y_train)
params = {
    "objective": "multiclass",
    "num_class": 3,
    "metric": "multi_logloss",
    "verbose": -1
}
model = lgb.train(params, train_dataset, num_boost_round=50)

# Predict
predictions = model.predict(X_test)
predicted_classes = [np.argmax(probs) for probs in predictions]

# Accuracy
correct_predictions = sum(int(a == b) for a, b in zip(y_test, predicted_classes))
accuracy = correct_predictions / len(y_test)
print(f"Model accuracy: {accuracy:.4f}")

# Confusion matrix
print("Confusion matrix:")
print(confusion_matrix(y_test, predicted_classes))

# Save test data + predictions as Parquet
test_rows = [list(f) + [int(a), int(p)] for f, a, p in zip(X_test, y_test, predicted_classes)]
schema = pa.schema([
    (feature_names[0], pa.float32()),
    (feature_names[1], pa.float32()),
    (feature_names[2], pa.float32()),
    (feature_names[3], pa.float32()),
    ("actual", pa.int8()),
    ("predicted", pa.int8())
])
columns = list(zip(*test_rows))  # transpose
table = pa.Table.from_arrays([pa.array(col, type=typ) for col, typ in zip(columns, schema.types)], schema=schema)
pq.write_table(table, "output/test_data.parquet")
print("Test data with predictions saved to output/test_data.parquet")

# Save feature importance image
importances = model.feature_importance()
features_sorted = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)

img_width, img_height = 400, 200
image = Image.new("RGB", (img_width, img_height), "white")
draw = ImageDraw.Draw(image)

draw.text((10, 10), "Feature Importance", fill="black")
y_position = 40
for name, score in features_sorted:
    draw.text((10, y_position), f"{name}: {score}", fill="blue")
    y_position += 30

image.save("output/feature_importance.png")
print("Feature importance image saved to output/feature_importance.png")

# Save model metadata
metadata = {
    "model_name": "LightGBM_Iris_Sklearn",
    "accuracy": round(accuracy, 4),
    "num_classes": 3,
    "num_features": 4,
    "num_test_samples": len(y_test)
}
with open("output/model_metadata.json", "w") as f:
    json.dump(metadata, f, indent=4)
print("Model metadata saved to output/model_metadata.json")

# Save model file
model.save_model("output/lightgbm_model.txt")
print("Trained model saved to output/lightgbm_model.txt")
