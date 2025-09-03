#!/bin/bash
set -e

# -------------------------------
# Function to detect Linux distro
# -------------------------------
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

DISTRO=$(detect_distro)
echo "Detected distribution: $DISTRO"
echo "Installing prerequisites..."

# -------------------------------
# Install system dependencies
# -------------------------------
case $DISTRO in
    "fedora"|"rhel"|"centos"|"rocky"|"almalinux")
        if command -v dnf >/dev/null 2>&1; then
            dnf install -y git gcc-toolset-13 make wget \
                openssl-devel bzip2-devel libffi-devel zlib-devel \
                python3.11 python3.11-devel python3-pip \
                rust cargo
            source /opt/rh/gcc-toolset-13/enable || true
        else
            yum install -y git gcc-toolset-13 make wget \
                openssl-devel bzip2-devel libffi-devel zlib-devel \
                python3.11 python3.11-devel python3-pip \
                rust cargo
            source /opt/rh/gcc-toolset-13/enable || true
        fi
        ;;
    "ubuntu"|"debian")
        apt update
        apt install -y git build-essential wget \
            libssl-dev libbz2-dev libffi-dev zlib1g-dev \
            python3.11 python3.11-dev python3-pip python3.11-venv \
            rustc cargo
        ;;
    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac

# -------------------------------
# Create and activate virtual env
# -------------------------------
python3.11 -m venv .venv
source .venv/bin/activate

# -------------------------------
# Upgrade pip and install packages
# -------------------------------
pip install --upgrade pip
pip install --prefer-binary --extra-index-url=https://wheels.developerfirst.ibm.com/ppc64le/linux -r requirements.txt
export LD_LIBRARY_PATH=./.venv/lib/python3.11/site-packages/openblas/lib:$LD_LIBRARY_PATH
# -------------------------------
# Run the environment test
# -------------------------------
echo "Running environment test..."
python3 xgboost_example.py

echo "\n ==== Running tests ==== \n"

python3 sub-test1.py
python3 sub-test2.py
python3 sub-test3.py
python3 sub-test4.py
