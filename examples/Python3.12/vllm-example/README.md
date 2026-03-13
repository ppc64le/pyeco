## ✅ Program : vLLM CPU Model Initialization and Environment Test

### Purpose:
Tests whether the **vLLM inference engine** can be successfully initialized and inspected in a **CPU-only environment**.  
The script verifies model loading, tokenizer access, engine configuration, CLI availability, and error handling without performing actual text generation.

### Packages used:
vllm  
wrapt  
subprocess  
os  
sys  
multiprocessing  

### Functionality:
- Sets CPU-friendly environment variables to run vLLM without GPU acceleration.
- Initializes the **IBM Granite 3.1 2B Instruct** model using vLLM.
- Prints environment configuration for debugging CPU execution.
- Verifies model configuration including:
  - Model name
  - Maximum sequence length
  - Supported tasks
- Wraps the `generate()` method using `wrapt` so generation calls are logged but **not executed**.
- Retrieves tokenizer information and vocabulary size if accessible.
- Inspects the vLLM engine configuration and device settings.
- Intentionally attempts to load a **nonexistent model** to confirm graceful error handling.
- Runs the `vllm --help` CLI command to verify that the vLLM command line interface is installed.
- Ensures the vLLM engine shuts down cleanly to prevent multiprocessing worker crashes.

### How to run the example :
```
chmod +x install_test_example.sh
./install_test_example.sh
```

### Notes:
- The script is configured for **CPU execution only**.
- Custom GPU operations are disabled using environment variables.
- Multiprocessing is configured with **spawn mode** to ensure compatibility with Python 3.12+.
- The `generate()` function is intentionally wrapped to avoid performing inference during the test.

### License:
This project is covered under **Apache 2.0 License**.