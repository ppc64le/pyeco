## ✅ Program : RandomForest to ONNX Iris Pipeline

### Purpose:
Trains a RandomForestClassifier on the Iris dataset, converts it to ONNX format, validates it, and performs inference using ONNX Runtime.

### Packages used:
skl2onnx onnx onnxruntime onnxconverter-common numpy scikit-learn

### Functionality:
- Loads and splits the Iris dataset into train/test sets.
- Trains a RandomForestClassifier using scikit-learn.
- Converts the trained model to ONNX format using skl2onnx.
- Validates the ONNX model using the ONNX checker.
- Performs inference on the test set using onnxruntime.
- Prints predictions to the console.

### How to run the example :
```
chmod +x install_test_example.sh 
./install_test_example.sh
```
### License: 
It's covered under Apache 2.0 licenses
