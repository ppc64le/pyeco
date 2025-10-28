#!/bin/bash

# Function to detect Linux distribution
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo $ID
    elif [ -f /etc/redhat-release ]; then
        echo "rhel"
    elif [ -f /etc/debian_version ]; then
        echo "debian"
    else
        echo "unknown"
    fi
}

# Install system dependencies based on distribution
DISTRO=$(detect_distro)

case $DISTRO in
    "fedora"|"rhel"|"centos"|"rocky"|"almalinux")
        if command -v dnf >/dev/null 2>&1; then
            sudo dnf install -y python3-protobuf python3.12-devel python3.12-pip libgfortran gcc gcc-c++ make
        else
            sudo yum install -y python3-protobuf python3.12-devel python3.12-pip libgfortran gcc gcc-c++ make
        fi
        ;;
    "ubuntu"|"debian")
        # Use: bash script.sh
        sudo apt update && sudo apt install -y \
        gcc g++ gfortran python3.12 python3.12-dev python3.12-venv python3-pip \
        python3-protobuf libopenblas-dev make

        ;;
    "sles")
        # Enable necessary modules
        sudo zypper refresh
        sudo zypper install -y python3-protobuf python3.12-devel python3-pip libgfortran gcc gcc-c++ make

        ;;
    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac


python3.12 -m venv venv
source venv/bin/activate

pip install --no-cache --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux -r requirements.txt

export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/libprotobuf/lib64:./venv/lib64/python3.12/site-packages/openblas/lib:$LD_LIBRARY_PATH

echo "USING Granite 3"
echo "Running: granite3-run.py"
python granite3-run.py

echo "Running: test-granite3-classification.py"
python test-granite3-classification.py

echo "USING Granite 4"
echo "Running: granite4-run.py"
python granite4-run.py

echo "Running: test-granite4-classification.py"
python test-granite4-classification.py
