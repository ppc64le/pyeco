#!/bin/bash
set -e

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
        export DEBIAN_FRONTEND=noninteractive
        sudo apt update -y
        sudo add-apt-repository ppa:deadsnakes/ppa -y
        sudo apt update -y
        sudo apt install -y python3.12 python3.12-dev python3.12-venv python3-pip
        ;;
    "sles")
        sudo zypper refresh
        # python312 is not in the default SLE_BCI repo; add the openSUSE Factory PowerPC repo
        # which provides python312/python312-pip/python312-devel for ppc64le
        sudo zypper addrepo --no-gpgcheck --check \
            "https://download.opensuse.org/repositories/devel:/languages:/python:/Factory/openSUSE_Factory_PowerPC/devel:languages:python:Factory.repo" \
            python312-repo || true
        sudo zypper --gpg-auto-import-keys refresh
        sudo zypper install -y python312 python312-pip python312-devel
        ;;
    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac

# -------------------------------
# Create and activate virtual env
# -------------------------------
python3.12 -m venv .venv
source .venv/bin/activate

# -------------------------------
# Upgrade pip and install packages
# -------------------------------
pip install --upgrade pip
pip install --prefer-binary --extra-index-url=https://wheels.developerfirst.ibm.com/ppc64le/linux -r requirements.txt

# -------------------------------
# Run the main example
# -------------------------------
echo "Running paddlepaddle_example.py ..."
python3 paddlepaddle_example.py

echo ""
echo "==== Running sub-tests ===="
echo ""

python3 sub-test1.py
python3 sub-test2.py
python3 sub-test3.py
