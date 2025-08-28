# pyeco
Python Ecosystem for Power Hints and Tips, Issue Tracking

NOTE:  We are starting to add a few requirements.txt base examples and a few tested programs using those to help people get
started.  Like with Pypi, there are a lot of possible permutations and combinations and not all will be tested, but the goal
is that there should be a clear path for major python toolset combinations.  We will also welcome additonal snippets or example
to help clarify.  We will ask for a DCO on any contributions.  We are also going to track any issues or requests here, although
note that as we are building this out, requests will be "as we can" while we are focused on some particular projects and combinations.

We appreciate your patience, and hopefully this guidance below is generalized, and you can see consolidated examples in the examples directory.

THANKS!!

--- 

Here's a **comprehensive and streamlined guide** to using **optimized Python packages on IBM Power systems**.

---

## 🚀 Optimized Python Packages on IBM Power: Complete Setup Guide

### ✅ 1. **Choose a Supported Python Version**
- Recommended: **Python 3.10, 3.11, or 3.12**
- Best support: **3.11 and 3.12** (most packages available)

---

### 🧪 2. **Create a Virtual Environment**
This isolates dependencies and avoids system conflicts:
```bash
python3.12 -m venv venv
source venv/bin/activate
```

---

### 📦 3. **Install Packages from IBM’s Optimized Wheel Repository**
Use `--prefer-binary` to prioritize prebuilt Power wheels:
```bash
pip install --prefer-binary <package-name> \
  --extra-index-url=https://wheels.developerfirst.ibm.com/ppc64le/linux
```

- This pulls from IBM’s Power-optimized wheel repo.
- Any `noarch` dependencies will still come from PyPI.

---

### 🔍 4. **Browse Available Packages (Optional)**
Use `devpi-client` to explore the repository:
```bash
pip install devpi-client
devpi use https://wheels.developerfirst.ibm.com/ppc64le/linux
devpi list
```

---

### 🛠️ 5. **Set `LD_LIBRARY_PATH` for Native Libraries**
Some packages (e.g., TensorFlow, PyTorch, OpenBLAS) require shared libraries at runtime.

If you encounter errors like:
```
ImportError: libXYZ.so: cannot open shared object file
```
Set the path to your native libraries:
```bash
export LD_LIBRARY_PATH=/path/to/libs:$LD_LIBRARY_PATH
```

💡 Use `ldd $(which python)` or `ldd <binary>` to check for missing `.so` files.

---

### 🧰 6. **Troubleshooting Tips from the Community**
- If a package fails to install:
  ```bash
  pip install --prefer-binary --no-cache-dir <package-name>
  ```
- Ensure you're using the correct Python version.
- If a package is missing, request it via:
  - [IBM TechXchange thread](https://community.ibm.com/community/user/discussion/unleash-the-power-of-ai-with-optimized-python-packages-for-ibm-power)

---

### 🧼 7. **Best Practices**
- Always use a virtual environment.
- Keep tools up to date:
  ```bash
  pip install --upgrade pip setuptools
  ```
- Use `--prefer-binary` to avoid unnecessary source builds.

---
