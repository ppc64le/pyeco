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
            sudo dnf install python3.12-devel python3.12-pip libatomic -y

        else
            sudo yum install python3.12-devel python3.12-pip libatomic -y
        fi
        ;;
    "ubuntu"|"debian")
        # Use: bash script.sh
        export DEBIAN_FRONTEND=noninteractive 
        sudo apt update &&  sudo apt install -y \
        python3.12 python3.12-dev python3.12-venv python3-pip libatomic\
        ;;
    "sles")
        sudo zypper refresh
        sudo zypper install -y python312 python312-pip python312-devel libatomic
        ;;
    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac

python3.12 -m venv venv
source venv/bin/activate

export VLLM_USE_CUSTOM_OPS=0

pip install --no-cache --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux -r requirements.txt

python vllm_example.py

echo "====Testing===="
# VLLM needs GPU so just running basic tests
python sub-test1.py
python sub-test2.py
python sub-test3.py
