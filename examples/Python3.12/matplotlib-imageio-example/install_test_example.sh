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
            sudo dnf install -y python3.12 python3.12-devel python3.12-pip
        else
            sudo yum install -y python3.12 python3.12-devel python3.12-pip
        fi
        ;;
    "ubuntu"|"debian")
        export DEBIAN_FRONTEND=noninteractive
        sudo apt update
        sudo apt install -y python3.12 python3.12-dev python3-pip python3.12-venv
        ;;
    "sles")
        sudo zypper refresh
        sudo zypper install -y python312 python312-pip python312-devel 
        ;;
    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac

# Create and activate virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install from requirements.txt with IBM ppc64le repository
pip install --prefer-binary --extra-index-url=https://wheels.developerfirst.ibm.com/ppc64le/linux -r requirements.txt

# Upgrade pip
pip install --upgrade pip

# Run Python scripts
printf "\nRunning matplotlib-imageio-example.py\n"
python3.12 matplotlib-imageio-example.py

printf "\nRunning sub-test1.py\n"
python3.12 sub-test1.py

printf "\nRunning sub-test2.py\n"
python3.12 sub-test2.py

printf "\nRunning sub-test3.py\n"
python3.12 sub-test3.py

