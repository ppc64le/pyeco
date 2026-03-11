## Program : TensorFlow Environment Diagnostics and Basic Training Test

### Purpose:
Validates a TensorFlow installation by checking version details, available hardware devices (CPU/GPU), running basic tensor operations, training a small Keras model, and verifying model save/load functionality.

### Packages used:

tensorflow numpy os

### Functionality:
- Configures TensorFlow environment variables to control logging verbosity and GPU memory allocation behavior.
- Prints TensorFlow version information and verifies whether the build supports CUDA.
- Lists available physical devices including CPUs and GPUs.
- Enables TensorFlow device placement logging to show where operations are executed.
- Performs a basic matrix multiplication using TensorFlow tensors on GPU if available, otherwise CPU.
- Trains a small Keras neural network model using randomly generated NumPy data.
- Displays the final training loss after model training.
- Saves the trained model in `.keras` format and reloads it to verify model persistence.
- Runs a prediction using the reloaded model to confirm successful loading.
- Provides clear diagnostic sections to help verify that TensorFlow and its core components are functioning properly.

### How to run the example :
```
chmod +x install_test_example.sh
./install_test_example.sh
```

### License:
It's covered under Apache 2.0 licenses