## ✅ Program : vLLM Model and Environment Validation Script

### Purpose:
Validates loading and basic usage of a vLLM model, wraps the generate method to intercept calls, inspects tokenizer and engine details, tests error handling on invalid models, and verifies the availability of the vllm CLI tool.

### Packages used:
vllm wrapt

### Functionality:
- Loads a vLLM model with specified settings.
- Displays model configuration and supported task information.
- Wraps the .generate() function to log invocation attempts without executing them.
- Retrieves tokenizer class information and vocabulary size when available.
- Checks the engine type, device setup, and operating mode.
- Attempts to load an invalid model name to ensure graceful failure.

### How to run the example :
```
chmod +x install_test_example.sh
./install_test_example.sh
```
### License: 
It's covered under Apache 2.0 licenses
