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
            sudo dnf install -y git gcc-toolset-13 make wget \
                openssl-devel bzip2-devel libffi-devel zlib-devel \
                python3.11 python3.11-devel python3-pip \
                rust cargo
            source /opt/rh/gcc-toolset-13/enable || true
        else
            sudo yum install -y git gcc-toolset-13 make wget \
                openssl-devel bzip2-devel libffi-devel zlib-devel \
                python3.11 python3.11-devel python3-pip \
                rust cargo
            source /opt/rh/gcc-toolset-13/enable || true
        fi
        ;;
    "ubuntu"|"debian")
        sudo apt update
        sudo apt install -y git build-essential wget \
            libssl-dev libbz2-dev libffi-dev zlib1g-dev \
            python3.11 python3.11-dev python3-pip python3.11-venv \
            rustc cargo
        ;;
    "sles")
        sudo zypper refresh
        sudo zypper install -y gcc13 python311 python311-pip gcc13-fortran gcc13-c++ zlib-devel cargo
        sudo zypper install -y git make wget libopenssl-devel libbz2-devel libbz2-1 libffi-devel rust 

        wget https://www.openssl.org/source/openssl-3.2.0.tar.gz
        tar -xzf openssl-3.2.0.tar.gz
        cd openssl-3.2.0
        ./Configure --prefix=/opt/openssl-3.2 --openssldir=/opt/openssl-3.2 linux-ppc64le
        make -j$(nproc)
        sudo make install_sw
        cd ..

        export LD_RUN_PATH=/opt/openssl-3.2/lib
        export LD_LIBRARY_PATH=/opt/openssl-3.2/lib:$LD_LIBRARY_PATH

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
