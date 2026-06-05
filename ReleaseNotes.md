# DevPi V5

**Release Date:** May 29, 2026

## Overview

This release includes updates to 20+ Python packages across multiple Python versions (3.10 to 3.14), focusing on AI/ML frameworks, data processing libraries, web frameworks, and infrastructure tools.
---
 
## Supported Platforms

| Category           | Supported Options |
|--------------------|-------------------|
| Architecture       | ppc64le           |
| Operating Systems  | RHEL, Ubuntu, SLES |
| Processors         | Power9, Power10, Power11 |
| Python Versions    | 3.10 – 3.13<br>3.14 (Preview - for few packages) |


## 🚀 Major Updates
- Expanded PowerPC (ppc64le) wheel support, with updates covering more than 20 packages.
- Newly added packages include lingua_language_detector, rfc3161-client, pyjnius.

## Package Licenses and CVE Details

Detailed package license information and CVE disclosures are available at 
[Package Licenses and CVE Details](https://github.com/ppc64le/pyeco/blob/main/DevpiWheelsIndex.md)

## Package Version compatiblity

| Package | Version | Python Versions | Compatible Torch Version | 
|---------|---------|-----------------|-------------------------|
| **torchvision** | 0.22.1+ppc64le1 | 3.11, 3.13 | 2.6.0 | 
| **torchvision** | 0.24.0+ppc64le1 | 3.11 | 2.9.0 |
| **torchvision** | 0.24.1+ppc64le1 | 3.10, 3.12 | 2.9.x |
| **torchvision** | 0.24.1+ppc64le2 | 3.11, 3.12, 3.13, 3.14 | 2.9.x |
| **torchvision** | 0.25.0+ppc64le1 | 3.11, 3.14 | 2.9.0 |
| **torchtext** | 0.18.0+ppc64le1 | 3.12 | 2.5.1 |
| **torchaudio** | 2.7.1+ppc64le1 | 3.10, 3.11, 3.12, 3.13 | 2.7.1 | 
| **torchaudio** | 2.9.0+ppc64le1 | 3.10, 3.11, 3.12, 3.13, 3.14 | 2.9.0 | 
| **torchaudio** | 2.9.1+ppc64le2 | 3.10, 3.12, 3.13, 3.14 | 2.9.1 | 
| **torchaudio** | 2.9.1+ppc64le3 | 3.11 | 2.9.1 | 

## Prerequisites
- JDK is required for PyJNIus.

## Known Issues
- **vllm v0.21.0** requires xgrammar, which in turn depends on apache-tvm-ffi. Prebuilt wheels are not available for xgrammar and apache-tvm-ffi. As a result, both packages must be built from source, or development tools must be installed and available at runtime to compile these packages from source.
- All versions of **vllm** require `httptools==0.8.0`. Prebuilt wheels for `httptools==0.8.0` are not available, so development tools such as `gcc` and `g++` must be installed and available at runtime to compile this package from source.
- Ollama is not supported on Power9.
- spacy and thinc depend on the murmurhash, preshed, and srsly packages. Prebuilt wheels are not available for these dependencies. As a result, gcc, g++, and Python development headers (Python.h) must be installed and available at runtime to compile these packages from source.

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

## 🚫 Deprecation Notice: Python 3.9 Support
Support for Python 3.9 has been removed starting with this release.
If you’re still using Python 3.9, please plan to upgrade to Python 3.10 or later to ensure compatibility with future updates.

⚠️ Important

- Existing Python 3.9 wheels are still available temporarily.
- They will be removed in a future release.

## 🔒 Feedback and Support

We welcome your feedback. For bug reports or enhancement suggestions, please raise an issue in [PyEco repository](https://github.com/ppc64le/pyeco/).
