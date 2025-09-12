## ✅ Program 1 : Linear Regression with Serialization and System Info Visualization

### Purpose:
Trains a simple linear regression model on synthetic data, serializes model parameters with msgpack, evaluates performance, and displays system usage stats and evaluation metrics visually using Pillow.

### Packages used:
numpy, pandas, scikit-learn, msgpack, psutil, pillow

### Functionality:
- Generates synthetic regression data.
- Splits data into training and testing sets.
- Trains a linear regression model and predicts on test data.
- Calculates mean squared error (MSE) on predictions.
- Serializes and deserializes model coefficients and intercept using msgpack.
- Gathers CPU and memory usage with psutil.
- Creates and displays a simple image showing MSE and system usage stats with Pillow.
- Prints unpacked model parameters to the console.

## ✅ Program 2: IBM COS SDK Test 

### Purpose: 
Validates connectivity and basic operations using the IBM Cloud Object Storage SDK.

### Packages Used:
ibm-cos-sdk requests certifi urllib3 

### Functionality:
- Simulates a COS client setup.
- Lists buckets (mocked).
- Validates response structure.

## ✅ Program 3 : JWT Generation and Verification with RSA Keys

### Purpose:
Generates an RSA key pair, creates a JWT token signed with the private key, and verifies it using the corresponding public key. The JWT includes a timezone-aware expiration claim.

### Packages used:
PyJWT, cryptography

### Functionality:
- Generates an RSA private/public key pair.
- Creates a JWT payload containing user info and a UTC-based expiration time 5 minutes from creation.
- Signs the JWT using RS256 algorithm with the private key.
- Decodes and verifies the JWT signature using the public key.
- Prints the decoded payload if verification succeeds, or an error message if it fails.

## ✅ Program 4 : Scikit-learn to ONNX Conversion and Inference Test

### Purpose:
Trains a RandomForestClassifier on the Iris dataset, converts the model to ONNX format, runs inference using onnxruntime, and compares predictions to ground truth for validation.

### Packages used:
scikit-learn, skl2onnx, onnxruntime, numpy

### Functionality:
- Loads the Iris dataset and splits it into training and testing sets.
- Trains a RandomForestClassifier with 10 estimators.
- Converts the trained scikit-learn model to ONNX format using skl2onnx.
- Saves the ONNX model to disk.
- Runs inference on the test set using onnxruntime.
- Compares ONNX model predictions with actual test labels and calculates accuracy.
- Prints sample predictions for visual validation.

### How to run the example :
```
chmod +x install_test_example.sh
./install_test_example.sh
```
### License: 
It's covered under Apache 2.0 licenses
