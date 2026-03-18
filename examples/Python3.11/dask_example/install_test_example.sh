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
        set -euo pipefail

        # Non-interactive for RHEL-like
        if command -v dnf >/dev/null 2>&1; then
            sudo dnf install -y python3-protobuf python3.11-devel python3.11-pip
        else
            sudo yum install -y python3-protobuf python3.11-devel python3.11-pip
        fi
        ;;

    "ubuntu"|"debian")
        sudo apt-get update -y
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
        sudo apt-get install -y --no-install-recommends \
          build-essential \
          wget \
          ca-certificates \
          libssl-dev \
          zlib1g-dev \
          libncurses5-dev \
          libncursesw5-dev \
          libreadline-dev \
          libsqlite3-dev \
          libgdbm-dev \
          libbz2-dev \
          libexpat1-dev \
          liblzma-dev \
          libffi-dev \
          tk-dev

        PY_VER="3.11.8"
        wget "https://www.python.org/ftp/python/${PY_VER}/Python-${PY_VER}.tgz"
        tar -xzf Python-3.11.8.tgz
        cd Python-3.11.8
        ./configure --enable-optimizations
        make -j"$(nproc)"
        make altinstall
        cd ..
        ;;

    "sles")
        # Non-interactive zypper
        sudo zypper --non-interactive refresh
        sudo zypper --non-interactive install python311 python311-pip python311-devel
        ;;

    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac

# Create and activate virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install from requirements.txt with IBM ppc64le repository
pip install --prefer-binary --extra-index-url=https://wheels-staging.developerfirst.ibm.com/ppc64le/linux -r requirements.txt

# Upgrade pip
pip install --upgrade pip

# Run Python scripts
echo "Running environment test..."
python3 dask_example.py

echo " ==== Running sub-test1 ==== "
python3 sub-test1.py

echo " ==== Running sub-test2 ==== "
python3 sub-test2.py
