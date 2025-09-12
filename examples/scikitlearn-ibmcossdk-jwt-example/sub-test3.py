from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import onnxruntime as rt
import numpy as np

# Load dataset
iris = load_iris()
X = iris.data.astype(np.float32)
y = iris.target.astype(np.int64)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=10)
clf.fit(X_train, y_train)

# Convert to ONNX (fix protobuf warning by using int instead of bool)
initial_type = [('float_input', FloatTensorType([None, 4]))]
onnx_model = convert_sklearn(clf, initial_types=initial_type, options={id(clf): {'zipmap': 0}})
with open("rf_model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

# Run inference
sess = rt.InferenceSession("rf_model.onnx")
input_name = sess.get_inputs()[0].name
label_name = sess.get_outputs()[0].name
pred_onx = sess.run([label_name], {input_name: X_test})[0]

# Validate output
correct = np.sum(pred_onx == y_test)
total = len(y_test)
accuracy = correct / total * 100

print("ONNX model test completed.")
print(f"Prediction accuracy: {correct}/{total} ({accuracy:.2f}%)")

# Show sample predictions
print("\nSample predictions:")
for i in range(min(5, total)):
    print(f"Input: {X_test[i]} => Predicted: {pred_onx[i]}, Expected: {y_test[i]}")

