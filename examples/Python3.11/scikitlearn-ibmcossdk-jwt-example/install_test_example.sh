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
            echo "Installing packages using dnf..."
            sudo dnf install -y \
                python3.11 \
                python3.11-devel \
                --skip-broken --nobest
        else
            echo "dnf not found, attempting yum..."
            sudo yum install -y \
                python3.11 \
                python3.11-devel 
        fi
        ;;
    "ubuntu"|"debian")
        echo "Installing packages using apt..."
        export DEBIAN_FRONTEND=noninteractive 
        sudo apt update
        sudo apt install -y \
            python3.11 \
            python3.11-dev \
            python3.11-venv \
            python3-pip 
        ;;
    "sles")
        sudo zypper refresh
        sudo zypper install -y python311 python311-pip python311-devel
        ;;
    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac

# Create and activate virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install --prefer-binary --extra-index-url=https://wheels.developerfirst.ibm.com/ppc64le/linux-v2026.03.31 -r requirements.txt

# Upgrade pip
pip install --upgrade pip


# Run scripts
echo -e "\nRunning scikitlearn_ibmcossdk_jwt_example.py"
python3.11 scikitlearn_ibmcossdk_jwt_example.py

echo -e "\nRunning sub-test1.py"
python3.11 sub-test1.py

echo -e "\nRunning sub-test2.py"
python3.11 sub-test2.py

echo -e "\nRunning sub-test3.py"
python3.11 sub-test3.py
