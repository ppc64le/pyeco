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
            sudo dnf install python3.12-devel python3.12-pip -y
        else
            sudo yum install python3.12-devel python3.12-pip -y
        fi
        ;;
    "ubuntu"|"debian")
        # Use: bash script.sh
        export DEBIAN_FRONTEND=noninteractive
        sudo apt update -y
        sudo apt install -y python3.12 python3.12-venv python3.12-distutils
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

python3.12 -m venv venv
source venv/bin/activate

pip install --no-cache --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux -r requirements.txt

python torchaudio_example.py
python torchvision_example.py

echo "\n ==== Running tests ==== \n"

python sub-test1.py
python sub-test2.py

