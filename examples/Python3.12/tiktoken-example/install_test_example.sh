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
            dnf install gcc-toolset-13 python3.12-devel python3.12-pip gcc gcc-c++ gcc-gfortran xz cmake yum-utils openssl-devel bzip2-devel bzip2 libffi-devel \
            zlib-devel autoconf automake libtool cargo \
            pkgconf-pkg-config -y --skip-broken --nobest
            
            source /opt/rh/gcc-toolset-13/enable
        else
            sudo yum install gcc-toolset-13 python3.12-devel python3.12-pip gcc gcc-c++ gcc-gfortran xz cmake yum-utils openssl-devel bzip2-devel bzip2 libffi-devel \
            zlib-devel autoconf automake libtool cargo \
            pkgconf-pkg-config -y
            source /opt/rh/gcc-toolset-13/enable
        fi
        ;;
    "ubuntu"|"debian")
        # Use: bash script.sh
        export DEBIAN_FRONTEND=noninteractive
        sudo apt update &&  sudo apt install -y \
        gcc g++ gfortran python3.12 python3.12-dev python3.12-venv python3-pip \
        xz-utils cmake libssl-dev \
        libbz2-dev libbz2-1.0 libffi-dev zlib1g-dev autoconf automake libtool \
        cargo pkg-config
        ;;
    "sles")
        sudo zypper refresh
        sudo zypper install -y gcc gcc-fortran python312 python312-pip python312-devel gcc-c++
        sudo zypper install -y libgfortran5 make cmake autoconf automake libtool pkg-config cargo rust
        sudo zypper install -y xz libbz2-devel libbz2-1 libffi-devel zlib-devel openssl-devel
        ;;
    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac

python3.12 -m venv venv
source venv/bin/activate

pip install --no-cache --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux-v2026.06.0 -r requirements.txt
python tiktoken_example.py

echo "====Testing===="
python sub-test1.py
python sub-test2.py
python sub-test3.py


