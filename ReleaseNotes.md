# DevPi V4

**Release Date:** May 11, 2026

## Overview

This release includes updates to 170+ Python packages across multiple Python versions (3.9, to 3.14), focusing on AI/ML frameworks, data processing libraries, web frameworks, and infrastructure tools.
---
 
## Supported Platforms

| Category           | Supported Options |
|--------------------|-------------------|
| Architecture       | ppc64le           |
| Operating Systems  | RHEL, Ubuntu, SLES |
| Processors         | Power9, Power10, Power11 |
| Python Versions    | 3.9 – 3.13<br>3.14 (Preview - for few packages) |


## 🚀 Major Updates
- Significantly expanded PowerPC (ppc64le) wheel support, with updates covering more than 170 packages.
- Python 3.14 preview support introduced for 70+ packages.
- Newly added packages include polars, catboost, tiktoken, milvus‑lite, and tesserocr.
- NumPy updated with OpenBLAS v0.3.32 for improved performance.
- Torch family packages updated to leverage OpenBLAS v0.3.32.
- TensorFlow upgraded to the latest stable release (v2.18.1) with performance optimizations.
- 13 packages updated to newer versions addressing CVE security fixes.

## Package Licenses and CVE Details

Detailed package license information and CVE disclosures are available at 
[Package Licenses and CVE Details](https://github.com/ppc64le/pyeco/blob/main/DevpiWheelsIndex.md)

## Package Version compatiblity

| Package | Version | Python Versions | Compatible Torch Version | 
|---------|---------|-----------------|-------------------------|
| **torchvision** | 0.22.1+ppc64le1 | 3.11, 3.13 | 2.6.0 | 
| **torchvision** | 0.24.0+ppc64le1 | 3.11 | 2.9.0 |
| **torchvision** | 0.24.1+ppc64le2 | 3.10, 3.11, 3.13, 3.14 | 2.9.0 |
| **torchvision** | 0.25.0+ppc64le1 | 3.11, 3.14 | 2.9.0 |
| **torchtext** | 0.18.0+ppc64le1 | 3.12 | 2.5.1 |
| **torchaudio** | 2.7.1+ppc64le1 | 3.10, 3.11, 3.12, 3.13 | 2.7.1 | 
| **torchaudio** | 2.9.0+ppc64le1 | 3.10, 3.11, 3.12, 3.13, 3.14 | 2.9.0 | 
| **torchaudio** | 2.9.1+ppc64le2 | 3.10, 3.12, 3.13, 3.14 | 2.9.1 | 
| **torchaudio** | 2.9.1+ppc64le3 | 3.11 | 2.9.1 | 

## Known Issues
- Ollama is not supported on Power9.
- spacy and thinc depend on the murmurhash, preshed, and srsly packages. Prebuilt wheels are not available for these dependencies. As a result, gcc, g++, and Python development headers (Python.h) must be installed and available at runtime to compile these packages from source.

## 🔒 Security Fixes

### The following package updates include fixes for **multiple known security vulnerabilities (CVEs)** as documented in their respective upstream security advisories and release notes.

| Package Name | Updated Version | Security Impact |
|--------------|-----------------|-----------------|
| Brotli       | 1.2.0           | Addresses multiple CVEs related to malformed input handling and potential denial‑of‑service conditions |
| brotlicffi   | 1.2.0.1         | Includes CVE fixes inherited from Brotli core updates |
| cryptography | 46.0.7          | Fixes several high‑ and medium‑severity CVEs affecting certificate validation, key handling, and cryptographic primitives |
| distributed  | 2026.1.0        | Resolves CVEs related to task scheduling, authentication, and cluster communication |
| Django       | 5.2.13          | Includes security patches for multiple CVEs involving request parsing, authorization, and data validation |
| filelock     | 3.25.2          | Fixes CVEs related to race conditions and improper file locking behavior |
| multipart    | 1.3.1           | Addresses CVEs caused by unsafe multipart parsing and boundary validation |
| nbconvert    | 7.17.1          | Resolves CVEs related to unsafe template rendering and notebook conversion |
| onnx         | 1.21.0          | Fixes CVEs related to model parsing vulnerabilities and malformed graph handling |
| poetry       | 2.3.4           | Addresses CVEs involving dependency resolution and configuration parsing |
| sympy        | 1.15.0          | Includes CVE fixes for expression parsing and symbolic computation edge cases |
| tornado      | 6.5.5           | Fixes CVEs affecting HTTP request handling and WebSocket processing |
| ujson        | 5.12.0          | Resolves CVEs related to unsafe JSON deserialization and memory handling |

**Note:** This list highlights selected CVE fixes and is not exhaustive. 

## ⚠️ Python 3.9 Discontinuation Notice
- Please note that support for Python 3.9 wheels will be discontinued in an upcoming release.

## 🔒 Feedback and Support

We welcome your feedback. For bug reports or enhancement suggestions, please raise an issue in [PyEco repository](https://github.com/ppc64le/pyeco/).