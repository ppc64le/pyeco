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
            sudo dnf install gcc-toolset-13 python3.12-devel python3.12-pip libjpeg-turbo-devel numactl gcc gcc-c++ gcc-gfortran xz cmake yum-utils openssl-devel openblas-devel bzip2-devel bzip2 libffi-devel \
            zlib-devel autoconf automake libtool cargo \
            pkgconf-pkg-config fontconfig fontconfig-devel sqlite-devel -y --skip-broken --nobest
            
            source /opt/rh/gcc-toolset-13/enable
        else
            sudo yum install gcc-toolset-13 python3.12-devel python3.12-pip libjpeg-turbo-devel numactl gcc gcc-c++ gcc-gfortran xz cmake yum-utils openssl-devel openblas-devel bzip2-devel bzip2 libffi-devel \
            zlib-devel autoconf automake libtool cargo \
            pkgconf-pkg-config fontconfig fontconfig-devel sqlite-devel -y
            source /opt/rh/gcc-toolset-13/enable
        fi
        ;;
    "ubuntu"|"debian")
        # Use: bash script.sh
        sudo apt update &&  apt install -y \
        gcc g++ gfortran python3.12 python3.12-dev python3.12-venv python3-pip \
        libjpeg-turbo8-dev libnuma-dev \
        xz-utils cmake libssl-dev libopenblas-dev \
        libbz2-dev libbz2-1.0 libffi-dev zlib1g-dev autoconf automake libtool \
        cargo pkg-config fontconfig libfontconfig1-dev sqlite3 libsqlite3-dev libjpeg62
        ;;
    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac

python3.12 -m venv venv
source venv/bin/activate

export VLLM_USE_CUSTOM_OPS=0

pip install --no-cache --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux -r requirements.txt

pip install --no-cache --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux libprotobuf==4.25.8 openblas

export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/openblas/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/libprotobuf/lib64:$LD_LIBRARY_PATH

python vllm_example.py

echo "====Testing===="
# VLLM needs GPU so just running basic tests
python sub-test1.py
python sub-test2.py
python sub-test3.py
