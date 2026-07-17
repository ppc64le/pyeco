## ✅ Program : PaddlePaddle Classification Pipeline with System Stats

### Purpose:
Trains a simple PaddlePaddle neural network on synthetic classification data, evaluates predictions, performs basic analysis with scipy and pandas, and reports system resource usage.

### Packages used:

paddlepaddle scikit-learn scipy numpy pandas psutil Pillow

### Functionality:
- Generates synthetic classification data with scikit-learn and normalizes features.
- Defines and trains a simple 2-layer PaddlePaddle neural network using `paddle.nn.Layer`.
- Evaluates model accuracy on test data.
- Uses scipy to find the mode of the predicted classes.
- Creates a pandas DataFrame for predictions and true labels for inspection.
- Reports CPU and memory usage with psutil.

### How to run the example :
```
chmod +x install_test_example.sh
./install_test_example.sh
```
### License: 
It's covered under Apache 2.0 licenses
