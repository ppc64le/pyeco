## ✅ Program : Multi-Package Environment Integration Test

### Purpose:
Tests the interoperability of several advanced Python packages (Pillow, ml_dtypes, PyAV, and llvmlite) by running a pipeline that handles images, video encoding, custom numeric types, and LLVM IR execution.

### Packages used:
pillow ml_dtypes av llvmlite numpy

### Functionality:
- Creates and saves an in-memory PNG image using Pillow.
- Constructs a NumPy array with the ml_dtypes.float8_e5m2 type.
- Encodes a video frame from the image using PyAV with the rawvideo codec inside an AVI container.
- Parses and verifies a minimal LLVM IR function using llvmlite.
- Confirms successful execution of all steps in a single script.
- If you get errors about codecs (like mpeg4), it means your FFmpeg doesn’t support them. The tests will use other codecs.

### How to run the example :
```
chmod +x install_test_example.sh
./install_test_example.sh
```
### License: 
It's covered under Apache 2.0 licenses
