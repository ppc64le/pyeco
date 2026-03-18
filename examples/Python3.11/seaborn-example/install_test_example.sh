#!/bin/bash

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
            sudo dnf install -y python3.11 python3.11-devel python3-pip
        else
            sudo yum install -y python3.11 python3.11-devel python3-pip
        fi
        ;;
    "ubuntu"|"debian")
        export DEBIAN_FRONTEND=noninteractive
        sudo apt update
        sudo apt install -y python3.11 python3.11-dev python3-pip python3.11-venv
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

python3.11 -m venv .venv
source .venv/bin/activate

python3.11 -m pip install --no-cache --prefer-binary --extra-index-url https://wheels-staging.developerfirst.ibm.com/ppc64le/linux -r requirements.txt

WORKDIR=$(pwd)

cd $WORKDIR

# Run Python scripts
echo "Running environment test..."
python3 seaborn-example.py

echo " ==== Running sub-test1 ==== "
python3 sub-test1.py

echo " ==== Running sub-test2 ==== "
python3 sub-test2.py

echo " ==== Running sub-test3 ==== "
python3 sub-test3.py
