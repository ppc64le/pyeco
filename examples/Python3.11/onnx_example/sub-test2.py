import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import os

def test_skl2onnx_conversion():
    # Load dataset
    iris = load_iris()
    X, y = iris.data.astype(np.float32), iris.target

    # Train a simple model
    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(X, y)

    # Define the input type for the ONNX model
    initial_type = [('float_input', FloatTensorType([None, X.shape[1]]))]

    # Convert the model
    onnx_model = convert_sklearn(clf, initial_types=initial_type)
    print("Model successfully converted to ONNX format.")

    # Save ONNX model
    model_path = "rf_model.onnx"
    with open(model_path, "wb") as f:
        f.write(onnx_model.SerializeToString())
    print(f"ONNX model saved as: {model_path}")

if __name__ == "__main__":
    test_skl2onnx_conversion()

