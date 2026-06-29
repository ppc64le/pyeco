# AI Foundation 2Q26

**Release Date:** Jun 30, 2026

## Overview

This release includes updates to 1100+ Python packages across Python versions 3.11 and 3.12 focusing on AI/ML frameworks, data processing libraries, web frameworks, and infrastructure tools.
---
 
## Supported Platforms

| Category           | Supported Options |
|--------------------|-------------------|
| Architecture       | ppc64le           |
| Operating Systems  | RHEL, Ubuntu, SLES |
| Processors         | Power9, Power10, Power11 |
| Python Versions    | 3.11, 3.12 |


## 🚀 Major Updates
- Comprehensive PowerPC (ppc64le) wheel support with over 1100 packages.

## Package Licenses and CVE Details

Detailed package license information and CVE disclosures are available at 
[Package Licenses and CVE Details](https://github.com/ppc64le/pyeco/blob/v2026.06.0/DevpiWheelsIndex.md)

## Package Version Compatiblity

### PyTorch-based Packages

| Package | Version | Python Versions | Compatible PyTorch Version | 
|---------|---------|-----------------|-------------------------|
| **torchvision** | 0.22.1+ppc64le1 | 3.11, 3.12 | 2.6.0 | 
| **torchvision** | 0.24.0+ppc64le1 | 3.11 | 2.9.0 |
| **torchvision** | 0.24.0+ppc64le2 | 3.12 | 2.9.0 |
| **torchvision** | 0.24.1+ppc64le2 | 3.11, 3.12 | 2.9.x |
| **torchvision** | 0.25.0+ppc64le2 | 3.11, 3.12 | 2.9.0 |
| **torchtext** | 0.18.0+ppc64le1,  | 3.11 | 2.8.0 |
| **torchtext** | 0.18.0+ppc64le2,  | 3.12 | 2.8.0 |
| **torchaudio** | 2.7.1+ppc64le1 | 3.11, 3.12 | 2.7.1 | 
| **torchaudio** | 2.9.0+ppc64le1 | 3.11, 3.12 | 2.9.0 | 
| **torchaudio** | 2.9.1+ppc64le2 | 3.12 | 2.9.1 | 
| **torchaudio** | 2.9.1+ppc64le3 | 3.11 | 2.9.1 | 

### TensorFlow-based Packages

| Package | Version | Python Versions | Compatible TensorFlow Version | 
|---------|---------|-----------------|-------------------------|
| **tensorflow-io** | 0.35.0+ppc64le1 | 3.11 | 2.14.1 | 
| **tf2onnx** | 1.15.1+ppc64.e1, 1.16.1+ppc64le1 | 3.11,3.12 | 2.18.1 | 

### ONNX-based Packages
| Package | Version | Python Versions | Compatible ONNX Version | 
|---------|---------|-----------------|-------------------------|
| **skl2onnx** | 1.18.0+ppc64le1 | 3.11,3.12 | 1.17.0 | 


## Prerequisites
- JDK is required for PyJNIus.
- krb5-devel is required for request-kerberos and sparkmagic.
- Rust is required for apache-airflow.
- onnxconverter-common is required for skl2onnx v1.18.0.
- packaging is required for iminuit v2.28.0.

## ⚠️ Known Issues
### Platform Support 
- Ollama is not supported on Power9.

### Python Version Support 
- aesera v2.9.4 does not support Python v3.12.

### Missing Pre-built Wheels for Some Dependencies
Some packages in this release do not have pre-built wheels available for certain dependencies.
As a result, these dependencies must be compiled from source during installation.

**Requirements:**
Compilation requires the following development tools:
- `gcc`
- `g++`
- Python development headers

**Affected packages:**
- ansible_rulebook 1.1.*
- cforge v1.0.0b4
- cutadapt 5.1
- macs
- orange3 v3.38.1
- spacy
- tensorflow v2.14.1
- tensorflow-text v2.14.0
- thinc
- uvtools
  
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

## 🔒 Feedback and Support

We welcome your feedback. For bug reports or enhancement suggestions, please raise an issue in [PyEco repository](https://github.com/ppc64le/pyeco/).
