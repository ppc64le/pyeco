import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import onnx
import onnxruntime as ort
from onnxconverter_common.data_types import FloatTensorType as CommonFloatTensorType
import onnxruntime as rt
import os

def train_model():
    # Load dataset
    iris = load_iris()
    X, y = iris.data.astype(np.float32), iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

    # Train a simple model
    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(X_train, y_train)

    return clf, X_test, y_test

def convert_to_onnx(model, X_sample):
    initial_type = [('float_input', FloatTensorType([None, X_sample.shape[1]]))]
    onnx_model = convert_sklearn(model, initial_types=initial_type)

    # Save the model
    onnx_model_path = "rf_model.onnx"
    with open(onnx_model_path, "wb") as f:
        f.write(onnx_model.SerializeToString())
    print(f"ONNX model saved to: {onnx_model_path}")
    return onnx_model_path

def load_and_check_onnx_model(path):
    model = onnx.load(path)
    onnx.checker.check_model(model)
    print("ONNX model is valid.")
    return model

def run_inference(onnx_model_path, X_test):
    # Load model with onnxruntime
    sess = ort.InferenceSession(onnx_model_path)
    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name

    # Run inference
    predictions = sess.run([label_name], {input_name: X_test})[0]
    print("Predictions:", predictions)
    return predictions

def main():
    clf, X_test, y_test = train_model()
    onnx_path = convert_to_onnx(clf, X_test)
    load_and_check_onnx_model(onnx_path)
    run_inference(onnx_path, X_test.astype(np.float32))

if __name__ == "__main__":
    main()

