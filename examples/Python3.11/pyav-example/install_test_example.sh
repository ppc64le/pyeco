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
            sudo dnf install -y python3.11 python3.11-devel python3.11-pip
        else
            sudo yum install -y python3.11 python3.11-devel python3.11-pip 
        fi
        ;;
    "ubuntu"|"debian")
        export DEBIAN_FRONTEND=noninteractive 
        sudo apt update
        sudo apt install -y libglib2.0-0 python3.11 python3.11-dev python3-pip python3.11-venv 
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

pip install --no-cache --prefer-binary --extra-index-url https://wheels-staging.developerfirst.ibm.com/ppc64le/linux -r requirements.txt


# Run Python scripts
printf "\nRunning av-example.py\n"
python3.11 av-example.py

printf "\nRunning test1.py\n"
python3.11 sub-test1.py

printf "\nRunning test2.py\n"
python3.11 sub-test2.py

printf "\nRunning test3.py\n"
python3.11 sub-test3.py
