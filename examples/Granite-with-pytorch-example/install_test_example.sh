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
        sudo zypper install -y  libgfortran5 python312 python312-pip python312-devel gcc13 gcc13-fortran gcc13-c++ zlib-devel cargo kernel-default-devel make
        sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-13 100
        sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-13 100
        sudo update-alternatives --install /usr/bin/c++ c++ /usr/bin/g++-13 100
        sudo update-alternatives --install /usr/bin/gfortran gfortran /usr/bin/gfortran-13 100

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

echo "Running: granite3-sub-test1.py"
python granite3-sub-test1.py

echo "USING Granite 4"
echo "Running: granite4-run.py"
python granite4-run.py

echo "Running: granite4-sub-test1.py"
python granite4-sub-test1.py
