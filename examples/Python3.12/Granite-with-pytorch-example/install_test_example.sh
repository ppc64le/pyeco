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
            sudo dnf install -y python3-protobuf python3.12-devel python3.12-pip
        else
            sudo yum install -y python3-protobuf python3.12-devel python3.12-pip
        fi
        ;;
    "ubuntu"|"debian")
        # Use: bash script.sh
        export DEBIAN_FRONTEND=noninteractive
        sudo apt update && sudo apt install -y \
        python3.12 python3.12-dev python3.12-venv python3-pip \
        python3-protobuf

        ;;
    "sles")
        # Enable necessary modules
        sudo zypper refresh
        sudo zypper install -y python312 python312-pip python312-devel
        ;;
    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac


python3.12 -m venv venv
source venv/bin/activate

pip install --no-cache --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux-v2026.03.31 -r requirements.txt


echo "USING Granite 3"
echo "Running: granite3-example.py"
python granite3-example.py

echo "Running: granite3-sub-test1.py"
python granite3-sub-test1.py

echo "USING Granite 4"
echo "Running: granite4-example.py"
python granite4-example.py

echo "Running: granite4-sub-test1.py"
python granite4-sub-test1.py
