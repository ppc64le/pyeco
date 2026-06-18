# Welcome to IBM Power - Optimized Python Wheels 🚀

This readme is designed to help new users quickly understand, discover, and use optimized Python wheels for IBM Power (ppc64le) systems. Whether you are evaluating the ecosystem, setting up your environment, or building Python applications, this guide walks you step by step.

## 🧭 Your Path to Using Optimized Wheels

1. [**Understand the Value**](#1️⃣-understand-the-value-why-optimized-wheels-matter) - Why optimized wheels matter on IBM Power
2. [**Check Compatibility**](#2️⃣-check-compatibility-is-this-right-for-you) - Architecture, processors, and Python versions
3. [**Discover Available Wheels**](#3️⃣-discover-available-wheels-find-the-right-packages) - Find packages and versions easily
4. [**Install with pip**](#4️⃣-install-with-pip-familiar-workflow) - Use familiar workflows with DevPI
5. [**Explore Examples**](#5️⃣-learn-by-example--general-usage-applications) - General usage applications
6. [**Go Further**](#6️⃣-go-further-build-faster-easier-and-explore-the-ecosystem) - Build faster, easier and explore the Ecosystem


---

## 1️⃣ Understand the Value: Why Optimized Wheels Matter

Python wheels (.whl) are prebuilt binary distributions that install directly with pip, without local compilation.

IBM's wheels are:

- **Natively built** on IBM Power (not cross-compiled)
- **Optimized** for AI, ML, and scientific computing
- **Delivered** through a [DevPI repository](https://wheels.developerfirst.ibm.com/ppc64le/linux) that integrates seamlessly with pip

---

## 2️⃣ Check Compatibility: Is This Right for You?

Before getting started, confirm your environment:

### Supported Platforms

- **Architecture**: ppc64le
- **Processors**: Power9, Power10, Power11
- **Python Versions**: 3.10 - 3.13 (3.14 preview for few packages)

If your system matches the above, you're ready to proceed.

## 3️⃣ Discover Available Wheels: Find the Right Packages

### 🔍 Central Wheel Repository

This is your main entry point for available optimized wheels:

👉 **Wheel Repository (DevPI)**:

https://wheels.developerfirst.ibm.com/ppc64le/linux

ℹ️ **Note**: This page shows only the latest version of each package.

👉 **Simple Index (All versions)**:

To view all available wheel versions for a package, refer to the [Simple Index](https://wheels.developerfirst.ibm.com/ppc64le/linux/+simple/) on the DevPI server, which provides the complete version history for that package.

📝 **Note: Wheel Version Suffixes**

IBM Power wheels use a version suffix (for example, `ppc64le1`) to identify build updates. When a wheel is rebuilt for the same upstream package version, the suffix is incremented (`ppc64le2`, `ppc64le3`, etc.). This allows incremental improvements while preserving the original upstream version number and clearly distinguishing updated builds.

### 📦 Complete Package & Version Indexes

To explore all available versions, Python compatibility, and licenses, use the indexes below:

- [DevPiWheelsIndex.md](https://github.com/ppc64le/pyeco/blob/main/DevpiWheelsIndex.md) - Full list of wheels with versions, build suffixes, licenses and associated CVEs
- [**Python version–specific indexes**](https://github.com/ppc64le/pyeco/tree/main/DevpiWheelsIndex) - Quickly filter wheels for:
  - Python 3.9
  - Python 3.10
  - Python 3.11
  - Python 3.12
  - Python 3.13
  - Python 3.14

## 4️⃣ Install with pip: Familiar Workflow

The optimized wheel repository acts as a **Power-aware extension to PyPI**, allowing you to use standard pip install commands while automatically selecting compatible IBM Power wheels when available without requiring any changes to your existing Python tooling

### Installation using the IBM Power DevPI Repository

Use `--prefer-binary` to prioritize prebuilt Power wheels:

```bash
pip install --prefer-binary <package-name> \
  --extra-index-url=https://wheels.developerfirst.ibm.com/ppc64le/linux
```

- This pulls from IBM's Power-optimized wheel repo.
- Any noarch dependencies will still come from PyPI.

👉 **Browse Available Packages (Optional)**: Use devpi-client to explore the repository:

```bash
pip install devpi-client
devpi use https://wheels.developerfirst.ibm.com/ppc64le/linux
devpi list
```

💡 **Tip**: You no longer need to set LD_LIBRARY_PATH when using Power manylinux wheels. Native dependencies are bundled automatically, so packages install cleanly and work consistently across Linux distributions such as SLES, Ubuntu, and RHEL.

📝 **Note**: Legacy wheels that do not support manylinux still require LD_LIBRARY_PATH to be set for correct execution.

### Troubleshooting Tips 

- If a package fails to install, try forcing binary wheels and disabling cache:

  ```bash
  pip install --prefer-binary --no-cache-dir <package-name> \
  --extra-index-url=https://wheels.developerfirst.ibm.com/ppc64le/linux
  ```

- Ensure you're using the correct Python version.

  ```bash
  python --version
  ```

- If a package is missing, request it via [IBM Power ISV ecosystem enablement form](https://www.ibm.com/power/resources/isv/enablement-request/)

- Most Python packages (e.g., TensorFlow, PyTorch) ship as manylinux wheels, which include all required shared libraries so normally, you don't need to set LD_LIBRARY_PATH. If you installed a non-manylinux wheel, you might see errors like: 

  ```
  ImportError: libXYZ.so: cannot open shared object file
  ```

  Set the path to your native libraries:

  ```bash
  export LD_LIBRARY_PATH=/path/to/libs:$LD_LIBRARY_PATH
  ```

  Use `ldd $(which python)` or `ldd <binary>` to check for missing .so files.

### Best Practices

- Always use a virtual environment. This isolates dependencies and ensures a clean setup.

  ```bash
  python3.12 -m venv venv
  source venv/bin/activate
  ```

- Keep tools up to date:

  ```bash
  pip install --upgrade pip setuptools
  ```

- Use `--prefer-binary` to avoid unnecessary source builds.

## 5️⃣ Learn by Example:  General Usage Applications

Explore real-world examples built using Power-optimized wheels:

### 📘PyEco Repository

- **Package Index & Metadata**:

  https://github.com/ppc64le/pyeco

- **General Usage Examples**: 

  https://github.com/ppc64le/pyeco/tree/main/examples

These examples demonstrate:

- Best practices for Power systems
- Practical usage of optimized libraries

## 6️⃣ Go Further: Build faster, easier and explore the Ecosystem

By leveraging IBM Power - optimized python wheels, teams can:

- ⚡ Accelerate data analytics and ML pipelines
- 🧠 Improve deep learning and generative AI performance
- 🚀 Increase developer productivity by eliminating build-related issues

This curated ecosystem is continuously expanded based on real AI projects across the IBM Power ecosystem.

## ✅ Your Next Steps

- 🔎 Browse available wheels → [DevPI Repository](https://wheels.developerfirst.ibm.com/ppc64le/linux)
- 📦 Identify Python version specific packages → [Wheel Indexes](https://github.com/ppc64le/pyeco/tree/main/DevpiWheelsIndex)
- ▶️ Try examples → [PyEco Examples](https://github.com/ppc64le/pyeco/tree/main/examples)
- 🧪 Build and optimize your AI/ML workloads on IBM Power

**Welcome to a faster, easier Python experience on IBM Power.**
