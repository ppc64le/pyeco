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
- Ollama is not supported on Power9.
- spacy and thinc depend on the murmurhash, preshed, and srsly packages. Prebuilt wheels are not available for these dependencies. As a result, gcc, g++, and Python development headers (Python.h) must be installed and available at runtime to compile these packages from source. 

## 🚫 Deprecation Notice: Python 3.9 Support  
Support for Python 3.9 has been removed starting with this release.
If you’re still using Python 3.9, please plan to upgrade to Python 3.10 or later to ensure compatibility with future updates.

⚠️ Important

- Existing Python 3.9 wheels are still available temporarily.
- They will be removed in a future release.

## 🔒 Feedback and Support

We welcome your feedback. For bug reports or enhancement suggestions, please raise an issue in [PyEco repository](https://github.com/ppc64le/pyeco/).
