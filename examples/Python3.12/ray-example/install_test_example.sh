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
            sudo dnf install -y python3.12 python3.12-devel python3-pip 
        else
            sudo yum install -y python3.12 python3.12-devel python3-pip 
        fi
        ;;
    "ubuntu"|"debian")
        sudo apt-get update -y
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
        sudo apt install -y python3.12 python3.12-venv python3.12-dev python3.12-pip
        ;;
    "sles")
        sudo zypper refresh
        sudo zypper install -y python312 python312-pip

        ;;
    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac



python3.12 -m venv .venv
source .venv/bin/activate

python3.12 -m pip install --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux-v2026.03.31 -r requirements.txt

WORKDIR=$(pwd)

cd $WORKDIR

python3.12 ray-example.py

echo "\n ==== Running tests ==== \n"

python3.12 sub-test1.py
python3.12 sub-test2.py
python3.12 sub-test3.py
