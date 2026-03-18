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
            sudo dnf -y install gcc-toolset-13 python3.11-devel python3.11-pip -y --skip-broken --nobest
            source /opt/rh/gcc-toolset-13/enable
        else
            sudo yum install gcc-toolset-13 python3.11-devel python3.11-pip -y
            source /opt/rh/gcc-toolset-13/enable
        fi
        ;;
    "ubuntu"|"debian")
        # Use: bash script.sh
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
        sudo apt install -y software-properties-common curl lsb-release gnupg2  libgomp1

        sudo add-apt-repository ppa:deadsnakes/ppa -y
        sudo apt update -y  
        sudo apt update && apt install -y python3.11 python3.11-dev python3.11-venv python3-pip
        ;;
    "sles")
        sudo zypper refresh
        sudo zypper install -y gcc gcc-fortran python311 python311-pip python311-devel libjpeg62-devel gcc-c++ freetype2-devel
        sudo zypper install -y cargo cmake ncurses-devel gawk libopenssl-devel perl libgfortran5
        sudo zypper install -y zlib-devel libffi-devel readline-devel xz-devel sqlite3-devel libzip-devel bzip2 wget tar 
        ;;
    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac

# Create and activate virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install from requirements.txt with IBM ppc64le repository
pip install --prefer-binary --extra-index-url=https://wheels-staging.developerfirst.ibm.com/ppc64le/linux -r requirements.txt
# Upgrade pip
pip install --upgrade pip

# Run Python scripts
printf "\nRunning matplotlib-imageio-example.py\n"
python3.11 matplotlib-imageio-example.py

printf "\nRunning sub-test1.py\n"
python3.11 sub-test1.py

printf "\nRunning sub-test2.py\n"
python3.11 sub-test2.py

printf "\nRunning sub-test3.py\n"
python3.11 sub-test3.py
