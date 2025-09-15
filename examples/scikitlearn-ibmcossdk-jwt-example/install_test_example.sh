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
            echo "Installing packages using dnf..."
            sudo dnf install -y \
                cargo \
                cmake \
                python3.12 \
                python3.12-devel \
                ncurses \
                gcc \
                gcc-c++ \
                libjpeg-devel \
                gfortran \
                --skip-broken --nobest
        else
            echo "dnf not found, attempting yum..."
            sudo yum install -y \
                cargo \
                cmake \
                python3.12 \
                python3.12-devel \
                ncurses \
                gcc \
                gcc-c++ \
                libjpeg-devel \
                gfortran
        fi
        ;;
    "ubuntu"|"debian")
        echo "Installing packages using apt..."
        sudo apt update
        sudo apt install -y \
            cargo \
            cmake \
            python3.12 \
            python3.12-dev \
            python3.12-venv \
            python3-pip \
            gcc \
            g++ \
            libjpeg-dev \
            gfortran \
            libncurses-dev
        ;;
    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac

# Create and activate virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install --prefer-binary --extra-index-url=https://wheels.developerfirst.ibm.com/ppc64le/linux -r requirements.txt

# Install specific additional packages
pip install --prefer-binary \
    libprotobuf==4.25.8 \
    openblas \
    --extra-index-url=https://wheels.developerfirst.ibm.com/ppc64le/linux

# Upgrade pip
pip install --upgrade pip

# Export environment variables for runtime
export LD_LIBRARY_PATH=./.venv/lib/python3.12/site-packages/openblas/lib:./.venv/lib/python3.12/site-packages/libprotobuf/lib64:$LD_LIBRARY_PATH

# Run scripts
echo -e "\nRunning scikitlearn_ibmcossdk_jwt_example.py"
python3.12 scikitlearn_ibmcossdk_jwt_example.py

echo -e "\nRunning sub-test1.py"
python3.12 sub-test1.py

echo -e "\nRunning sub-test2.py"
python3.12 sub-test2.py

echo -e "\nRunning sub-test3.py"
python3.12 sub-test3.py
