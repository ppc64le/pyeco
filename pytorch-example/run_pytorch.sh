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
            sudo dnf install gcc-toolset-13 python3.11-devel python3.11-pip -y --skip-broken --nobest
            source /opt/rh/gcc-toolset-13/enable
        else
            sudo yum install gcc-toolset-13 python3.11-devel python3.11-pip -y
            source /opt/rh/gcc-toolset-13/enable
        fi
        ;;
    "ubuntu"|"debian")
        # Use: bash script.sh
        apt update -y
        apt install -y software-properties-common curl lsb-release gnupg2  libgomp1

        add-apt-repository ppa:deadsnakes/ppa -y
        apt update -y
        apt install -y python3.11 python3.11-venv python3.11-distutils libgfortran5 gcc-13
        ;;
    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac

python3.11 -m venv venv
source venv/bin/activate

pip install --no-cache --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux -r requirements.txt

pip install libprotobuf==4.25.8 openblas --no-cache --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux

export LD_LIBRARY_PATH=./venv/lib64/python3.11/site-packages/libprotobuf/lib64:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=./venv/lib64/python3.11/site-packages/openblas/lib:$LD_LIBRARY_PATH

python pytorch_example.py

echo "\n ==== Running tests ==== \n"

python sub-test1.py
python sub-test2.py
python sub-test3.py
