# PyECO Automated Example Runner

## Overview
`run_pyeco.sh` is a Docker-based automation script to run and validate PyECO example packages across multiple Linux platforms.  
It executes install/test scripts, collects logs, classifies results, and generates an Excel summary.

---

## Features
- Runs PyECO examples in Docker containers  
- Supports **UBI 9.6**, **Ubuntu**, and **SLES**
- Runs all packages or selected packages list
- Generates logs and Excel summary report

---

## Usage
```sh
# Help
./run_pyeco.sh --help

# Run All Packages
./run_pyeco.sh

# Run Selected Packages
./run_pyeco.sh selected_packages.txt
```
# selected_packages.txt rules:

- One package per line
- Blank lines and # comments ignored
- Partial name matching supported
  
# Output
- Logs are saved as:

```<platform>_<python>_<package>.log```

Output structure:

```
pyeco_run_<timestamp>/
├── logs/
│   ├── passed/
│   └── failed/
└── pyeco_summary.xlsx
```

Excel summary includes:

- Platform, Python version, Package, Status, Log file name
# Prerequisites
- Docker
- Bash
- Python 3 (openpyxl)
