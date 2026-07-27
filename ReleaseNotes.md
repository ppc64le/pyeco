# DevPi V7

**Release Date:** Jul 23, 2026

## Overview

This release includes updates to 50+ Python packages across multiple Python versions (3.10 to 3.14), focusing on AI/ML frameworks, data processing libraries, web frameworks, and infrastructure tools.

Additionally, wheels without local version identifiers (suffixes) are now provided for uv compatibility. These wheels are available alongside the corresponding versions that include local version suffixes.

---
 
## Supported Platforms

| Category           | Supported Options |
|--------------------|-------------------|
| Architecture       | ppc64le           |
| Operating Systems  | RHEL, Ubuntu, SLES |
| Processors         | Power9, Power10, Power11 |
| Python Versions    | 3.10 – 3.13<br>3.14 (Preview - for few packages) |


## 🚀 Major Updates
- Added over 150 wheels including: 
    - 6 new packages -  jq, paddlepaddle, networkx, mistral_common, setools and srsly.
    - Packaging fixes in 17 native library wheels.
    - TensorFlow v2.14.1 and its dependencies for UBI 8.10
 
## Package Licenses and CVE Details

Detailed package license information and CVE disclosures are available at 
[Package Licenses and CVE Details](https://github.com/ppc64le/pyeco/blob/main/DevpiWheelsIndex.md)

## Package Prerequisites
- JDK is required for PyJNIus. 
- ruamel.yaml is required for ruamel_yaml_clib.
- httpx is required for httpx_sse.
- TensorFlow is required for tensorflow-io-gcs-filesystem.
- TensorFlow v2.18.1 is compatible with flatbuffers v25.2.10.

## Package Version compatiblity

### PyTorch compatibility

| Package | Version | Python Versions | Compatible Torch Version | 
|---------|---------|-----------------|-------------------------|
| **torchvision** | 0.22.1 | 3.11, 3.13 | 2.6.0 | 
| **torchvision** | 0.24.0 | 3.11 | 2.9.0 |
| **torchvision** | 0.24.1 | 3.10, 3.12 | 2.9.x |
| **torchvision** | 0.24.1 | 3.11, 3.12, 3.13, 3.14 | 2.9.x |
| **torchvision** | 0.25.0 | 3.11, 3.14 | 2.9.0 |
| **torchtext** | 0.15.2 | 3.12 | 2.8.0 |
| **torchtext** | 0.16.2 | 3.10, 3.11 | 2.8.0 |
| **torchtext** | 0.18.0 | 3.10, 3.11, 3.12, 3.13 | 2.8.0 |
| **torchaudio** | 2.6.0 | 3.11, 3.12 | 2.6.0 |
| **torchaudio** | 2.7.1 | 3.10, 3.11, 3.12, 3.13 | 2.7.1 | 
| **torchaudio** | 2.8.0 | 3.12 | 2.8.0 |
| **torchaudio** | 2.9.0 | 3.10, 3.11, 3.12, 3.13, 3.14 | 2.9.0 | 
| **torchaudio** | 2.9.1 | 3.10, 3.11, 3.12, 3.13, 3.14 | 2.9.1 | 

For complete version compatibility information between PyTorch and its domain libraries, see the - [PyTorch - Domain libraries version compatibility matrix](https://github.com/pytorch/pytorch/wiki/PyTorch-Versions)
 
### Numpy compatibility

The following packages require **NumPy 1.26.4** and are not compatible with NumPy 2.x.

- bottleneck 1.3.5
- h5py 3.7.0, 3.10.0
- ml-dtypes 0.1.0, 0.2.0
- matplotlib 3.7.1
- numexpr 2.8.4, 2.8.7
- pandas 1.5.3, 2.1.1
- pyarrow 11.0.0
- scikit-image 0.19.3, 0.20.0, 0.22.0
- PyWavelets 1.4.1
- pyclaw 5.12.0

### setuptools compatibility

The following packages require **setuptools < 81** and may not function correctly with newer setuptools versions.
- milvus-lite
- paddlepaddle
- AWX 24.6.1
- setools
- xgboost

## ⚠️ Known Issues
### Platform Support 
- Ollama is not supported on Power9.

### Missing Pre-built Wheels for Some Dependencies
Some packages in this release do not have pre-built wheels available for certain dependencies.
As a result, these dependencies must be compiled from source during installation.

**Requirements:**
Compilation requires the following development tools:
- `gcc`
- `g++`
- Python development headers
- Rust and Cargo (required for apache-airflow)

**Affected packages:**
- ansible_rulebook 1.1.*
- autovizwidget 0.22.0
- cforge v1.0.0b4
- cutadapt 5.1
- lightgbm 3.3.2
- macs
- orange3 v3.38.1
- poetry 1.8.*
- sparkmagic 0.20.0
- tensorflow 2.14.1
- tensorflow-text 2.14.0
- uvtools
- apache-airflow (requires Rust and Cargo)

## 🔧 Troubleshooting

### milvus-lite 2.5.1
The following issues have been identified on ppc64le. If you encounter these problems in your environment, use the workaround below. If milvus-lite works without issues, no action is needed.

**Identified Issues:**
1. The bundled milvus executable may lack execute permissions.
2. The bundled `libgcc_s.so.1` may require a newer glibc version than available in some environments.

**If you face these issues, use the following workaround:**
```bash
pip install milvus-lite==2.5.1 --index-url=<your-index-url> && \
chmod 755 /opt/app-root/lib64/python3.12/site-packages/milvus_lite/lib/milvus && \
# Use the system libgcc_s.so.1 because the bundled copy requires a newer glibc.
mv /opt/app-root/lib64/python3.12/site-packages/milvus_lite/lib/libgcc_s.so.1 \
   /opt/app-root/lib64/python3.12/site-packages/milvus_lite/lib/libgcc_s.so.1.disabled
```

## 🗑️ Removed

### `LD_LIBRARY_PATH` Requirement

Previously, users installing non-manylinux wheels had to manually set `LD_LIBRARY_PATH` to point to native shared libraries, to avoid runtime errors such as:

```
ImportError: libXYZ.so: cannot open shared object file
```

All wheels provided in this repository are **manylinux-compliant** and bundle their required native dependencies directly. This means:

- No manual `LD_LIBRARY_PATH` configuration is needed.
- Packages install cleanly and run consistently across all supported Linux distributions (RHEL, Ubuntu, SLES).
- The related tip, note, and troubleshooting guidance for `LD_LIBRARY_PATH` have been removed from the README accordingly.

## 🚫 Deprecation Notice: Python 3.9 Support
Support for Python 3.9 has been removed starting with this release.
If you’re still using Python 3.9, please plan to upgrade to Python 3.10 or later to ensure compatibility with future updates.

⚠️ Important

- Existing Python 3.9 wheels are still available temporarily.
- They will be removed in a future release.

## 🔒 Feedback and Support

We welcome your feedback. For bug reports or enhancement suggestions, please raise an issue in [PyEco repository](https://github.com/ppc64le/pyeco/).
