import numpy as np
import onnx
import onnxruntime as ort
import os

def test_onnx_loading_and_inference(onnx_model_path):
    print(f"Loading ONNX model from: {onnx_model_path}")

    # Load and check the ONNX model
    model = onnx.load(onnx_model_path)
    onnx.checker.check_model(model)
    print("ONNX model is valid.")

    # Create inference session
    sess = ort.InferenceSession(onnx_model_path)
    input_name = sess.get_inputs()[0].name

    # Create dummy input based on model input shape
    input_shape = sess.get_inputs()[0].shape
    # Replace None with 1 (batch size)
    input_shape = [1 if dim is None else dim for dim in input_shape]
    dummy_input = np.random.randn(*input_shape).astype(np.float32)

    print(f"Running inference with dummy input of shape {dummy_input.shape}...")
    outputs = sess.run(None, {input_name: dummy_input})
    print(f"Inference output type: {type(outputs)}, number of outputs: {len(outputs)}")
    print("Inference successful.")

if __name__ == "__main__":
    model_path = "rf_model.onnx"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"ONNX model file '{model_path}' not found! Please run the training/conversion script first.")
    test_onnx_loading_and_inference(model_path)

