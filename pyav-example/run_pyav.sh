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
            dnf install -y python3.12 python3.12-devel python3.12-pip gcc-toolset-13 libjpeg-devel freetype-devel
            source /opt/rh/gcc-toolset-13/enable
        else
            yum install -y python3.12 python3.12-devel python3.12-pip gcc-toolset-13 libjpeg-devel
            source /opt/rh/gcc-toolset-13/enable
        fi
        ;;
    "ubuntu"|"debian")
        apt update
        apt install -y python3.12 python3.12-dev python3-pip python3.12-venv gcc libjpeg-dev libgfortran5 g++
        ;;
    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac

# Create and activate virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Manually set LD_LIBRARY_PATH for the libraries installed via pip
echo "Setting LD_LIBRARY_PATH to include all required libraries..."
export LD_LIBRARY_PATH="./.venv/lib/python3.12/site-packages/ffmpeg/lib:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH="./.venv/lib/python3.12/site-packages/libvpx/lib:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH="./.venv/lib/python3.12/site-packages/lame/lib:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH="./.venv/lib/python3.12/site-packages/opus/lib:$LD_LIBRARY_PATH"

# Run Python scripts
printf "\nRunning av-example.py\n"
python3.12 av-example.py

printf "\nRunning test1.py\n"
python3.12 test1.py

printf "\nRunning test2.py\n"
python3.12 test2.py
