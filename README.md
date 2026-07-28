# Welcome to IBM Power - Optimized Python Wheels 🚀

This readme is designed to help new users quickly understand, discover, and use optimized Python wheels for IBM Power (ppc64le) systems. Whether you are evaluating the ecosystem, setting up your environment, or building Python applications, this guide walks you step by step.

## 🧭 Your Path to Using Optimized Wheels

1. [**Understand the Value**](#1️⃣-understand-the-value-why-optimized-wheels-matter) - Why optimized wheels matter on IBM Power
2. [**Check Compatibility**](#2️⃣-check-compatibility-is-this-right-for-you) - Architecture, processors, and Python versions
3. [**Discover Available Wheels**](#3️⃣-discover-available-wheels-find-the-right-packages) - Find packages and versions easily
4. [**Install with pip**](#4️⃣-install-with-pip-familiar-workflow) - Use familiar workflows with DevPI
5. [**Install with uv**](#5️⃣-install-with-uv-fast-modern-package-management) - Fast, modern package management with uv
6. [**Explore Examples**](#6️⃣-learn-by-example--general-usage-applications) - General usage applications
7. [**Go Further**](#7️⃣-go-further-build-faster-easier-and-explore-the-ecosystem) - Build faster, easier and explore the Ecosystem


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

📝 **Note: Wheel Versions and Suffixes**

IBM Power wheels are published in two forms:

| Wheel type | Example version | Purpose |
|---|---|---|
| **Suffix wheel** | `2.2.6+ppc64le1`, `2.2.6+ppc64le2` | Identifies a specific IBM Power build. The wheel with the **highest suffix is the latest build**. |
| **Suffix-free wheel** | `2.2.6` | A fixed, stable build provided for compatibility with tools like `uv` that work best without version suffixes. |

- The **suffix** (`ppc64le1`, `ppc64le2`, …) is incremented each time a wheel is rebuilt for the same upstream version, for example to pick up security patches or compiler improvements.
- The **suffix-free** wheel is a **convenience build** for simple installs. If you need build traceability or want to ensure a specific build is used, always pin to the explicit suffixed version (e.g. `numpy==2.2.6+ppc64le1`).
- Both forms are available simultaneously — you can use either depending on your workflow.

**Choosing the right version**:

| Goal | What to install |
|---|---|
| Latest IBM Power build | Highest-suffix version, e.g. `2.2.6+ppc64le2` |
| Simple install with no suffix needed (e.g. with `uv`) | Suffix-free version `2.2.6` |
| A specific known build | Full suffixed version, e.g. `2.2.6+ppc64le1` |

**Pinning to a specific build**: Specify the full suffixed version explicitly:

```bash
# pip
pip install "numpy==2.2.6+ppc64le2" \
  --extra-index-url=https://wheels.developerfirst.ibm.com/ppc64le/linux

# uv
uv pip install "numpy==2.2.6+ppc64le2" \
  --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux \
  --index-strategy unsafe-best-match
```

To see all available builds for a package, browse the [Simple Index](https://wheels.developerfirst.ibm.com/ppc64le/linux/+simple/).

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

## 5️⃣ Install with uv: Fast, Modern Package Management

[`uv`](https://github.com/astral-sh/uv) is an extremely fast Python package manager written in Rust. It is a drop-in replacement for `pip` and `pip-tools`, and works seamlessly with the IBM Power DevPI repository.

### Installing uv

```bash
# Using pip
pip install uv

# Or using the official standalone installer (Linux/macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installation using the IBM Power DevPI Repository

IBM Power wheels are published as **suffix-free** builds (e.g. `2.2.6`) in addition to suffixed builds (e.g. `2.2.6+ppc64le1`, `2.2.6+ppc64le2`). The suffix-free wheel is a **fixed, stable build** that lets `uv` install without needing to know the exact suffix. See the [Wheel Versions and Suffixes](#-note-wheel-versions-and-suffixes) note in section 3 for full details.

Use `--extra-index-url` and `--index-strategy unsafe-best-match` to prefer Power-optimized wheels when available:

```bash
uv pip install --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux \
  --index-strategy unsafe-best-match \
  --prefer-binary \
  <package-name>
```

- **`--index-strategy unsafe-best-match`** — allows `uv` to select the best-matching wheel across all configured indexes (PyPI + DevPI), prioritising Power-optimized wheels.
- **`--prefer-binary`** — skips source builds and installs prebuilt wheels whenever possible.
- Any `noarch` dependencies will still be resolved from PyPI.

**Pinning to a specific IBM Power build**: Specify the full suffixed version if you need a particular build:

```bash
uv pip install "numpy==2.2.6+ppc64le2" \
  --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux \
  --index-strategy unsafe-best-match
```

### Using `uv add` with pyproject.toml

`uv add` is the recommended way to manage dependencies in a `uv`-based project. It installs the IBM Power wheel but records only the **base version** (without the local suffix) in `pyproject.toml`, keeping the project portable:

```bash
uv add numpy==2.2.6 --index https://wheels.developerfirst.ibm.com/ppc64le/linux
# Installed: numpy==2.2.6+ppc64le2
# Recorded in pyproject.toml: "numpy==2.2.6"
```

This is correct behaviour. PEP 440 local version segments (`+ppc64le2`) are **not permitted in dependency specifiers**, so `uv` intentionally strips them when writing to `pyproject.toml`.

**Will `uv sync` from that `pyproject.toml` work on IBM Power?**

Yes. When `uv` later resolves `numpy==2.2.6` (e.g. via `uv sync`), PEP 440 specifies that a local version segment is **ignored during dependency resolution** — so `numpy==2.2.6` matches `numpy==2.2.6+ppc64le2` on the IBM DevPI index and the correct IBM Power wheel is installed.

```
uv sync
  → resolves  numpy==2.2.6  (from pyproject.toml)
  → matches   numpy==2.2.6+ppc64le2  on IBM DevPI  ✅
  → installs  numpy==2.2.6+ppc64le2
```

> ⚠️ **Portability note**: If the same `pyproject.toml` is used on a non-ppc64le system without the IBM DevPI index configured, `uv` will fall back to the PyPI wheel for `numpy==2.2.6`. Ensure the IBM DevPI index is configured for all IBM Power environments.

**Verifying which build was actually installed**

After running `uv add` or `uv sync`, use any of the following to confirm the exact build installed:

```bash
# Shows the full installed version including the local suffix
uv pip show numpy

# Lists all installed packages with their full versions
uv pip freeze | grep numpy

# Inspect the installed distribution metadata directly
python -c "import importlib.metadata; print(importlib.metadata.version('numpy'))"
```

Expected output (on IBM Power with the DevPI index):
```
2.2.6+ppc64le2
```

If the output shows `2.2.6` without a suffix, the PyPI wheel was picked up instead of the IBM Power build — verify your index configuration.

### Using a Virtual Environment with uv

```bash
# Create a virtual environment
uv venv .venv

# Activate it
source .venv/bin/activate          

# Install packages into the virtual environment
uv pip install --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux \
  --index-strategy unsafe-best-match \
  --prefer-binary \
  <package-name>
```

### Installing from a requirements file

```bash
uv pip install -r requirements.txt \
  --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux \
  --index-strategy unsafe-best-match \
  --prefer-binary
```

### Troubleshooting Tips

- If a package is not found, verify the package name against the [Simple Index](https://wheels.developerfirst.ibm.com/ppc64le/linux/+simple/).
- Force a fresh install and bypass the cache:

  ```bash
  uv pip install --no-cache --reinstall \
    --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux \
    --index-strategy unsafe-best-match \
    <package-name>
  ```

- Check the installed `uv` version:

  ```bash
  uv --version
  ```

### Best Practices

- Always use `uv venv` to create isolated environments per project.
- Pin your dependencies with `uv pip freeze > requirements.txt` for reproducible builds.
- Keep `uv` up to date:

  ```bash
  pip install --upgrade uv
  ```

---

## 6️⃣ Learn by Example:  General Usage Applications

Explore real-world examples built using Power-optimized wheels:

### 📘PyEco Repository

- **Package Index & Metadata**:

  https://github.com/ppc64le/pyeco

- **General Usage Examples**: 

  https://github.com/ppc64le/pyeco/tree/main/examples

These examples demonstrate:

- Best practices for Power systems
- Practical usage of optimized libraries

## 7️⃣ Go Further: Build faster, easier and explore the Ecosystem

By leveraging IBM Power - optimized python wheels, teams can:

- ⚡ Accelerate data analytics and ML pipelines
- 🧠 Improve deep learning and generative AI performance
- 🚀 Increase developer productivity by eliminating build-related issues

This curated ecosystem is continuously expanded based on real AI projects across the IBM Power ecosystem.

## ✅ Your Next Steps

- 🔎 Browse available wheels -> [DevPIWheelsIndex.md](https://github.com/ppc64le/pyeco/blob/main/DevpiWheelsIndex.md)
- 📦 Identify Python version specific packages → [Wheel Indexes](https://github.com/ppc64le/pyeco/tree/main/DevpiWheelsIndex)
- ▶️ Try examples → [PyEco Examples](https://github.com/ppc64le/pyeco/tree/main/examples)
- 🧪 Build and optimize your AI/ML workloads on IBM Power

**Welcome to a faster, easier Python experience on IBM Power.**
