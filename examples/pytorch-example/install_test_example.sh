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
            sudo dnf install python3.11-devel python3.11-pip -y --skip-broken --nobest
        else
            sudo yum install python3.11-devel python3.11-pip -y
        fi
        ;;
    "ubuntu"|"debian")
        add-apt-repository ppa:deadsnakes/ppa -y
        sudo apt update -y
        sudo apt install -y python3.11 python3.11-venv python3.11-distutils
        ;;
    "sles")
        sudo zypper refresh
        sudo zypper install -y python311 python311-pip
        ;;
    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac

python3.11 -m venv venv
source venv/bin/activate

pip install --no-cache --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux -r requirements.txt

python pytorch_example.py

echo "\n ==== Running tests ==== \n"

python sub-test1.py
python sub-test2.py
python sub-test3.py
