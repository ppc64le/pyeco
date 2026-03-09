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

        echo "Building Python 3.10 from source for RHEL-based system..."

        if command -v dnf >/dev/null 2>&1; then
            PKG_MGR="dnf"
            sudo dnf groupinstall -y "Development Tools"
        else
            PKG_MGR="yum"
            sudo yum groupinstall -y "Development Tools"
        fi

        sudo $PKG_MGR install -y \
            wget openssl-devel bzip2-devel libffi-devel \
            zlib-devel xz-devel ncurses-devel sqlite-devel gcc-c++ make gcc 

        wget https://www.python.org/ftp/python/3.10.15/Python-3.10.15.tgz
        tar xf Python-3.10.15.tgz
        cd Python-3.10.15
        ./configure --enable-optimizations
        make -j$(nproc)
        sudo make altinstall
        cd ..
        rm -rf Python-3.10.15*
        ;;

    "ubuntu"|"debian")
        export DEBIAN_FRONTEND=noninteractive
        sudo apt update && sudo apt install -y \
        python3.10 python3.10-dev python3.10-venv python3-pip \
        python3-protobuf
        ;;

    "sles")
        sudo zypper refresh
        sudo zypper install -y gcc gcc-c++ make wget curl tar gzip awk gawk \
            patch which \
            libopenssl-devel \
            zlib-devel \
            ncurses-devel \
            readline-devel \
            sqlite3-devel \
            libffi-devel \
            xz-devel \
            libbz2-devel
        wget https://www.python.org/ftp/python/3.10.15/Python-3.10.15.tgz
        tar xf Python-3.10.15.tgz
        cd Python-3.10.15
        ./configure --enable-optimizations
        make -j$(nproc)
        sudo make altinstall
        cd ..
        rm -rf Python-3.10.15*
        ;;

    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac


# Create and activate virtual environment
python3.10 -m venv .venv
source .venv/bin/activate

# Install from requirements.txt with IBM ppc64le repository
python3 -m pip install --upgrade pip

# Install requirements
python3 -m pip install --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux -r requirements.txt

# Run Python scripts
echo "Running environment test..."
python3 keras-example.py

echo " ==== Running sub-test1 ==== "
python3 sub-test1.py

echo " ==== Running sub-test2 ==== "
python3 sub-test2.py

echo " ==== Running sub-test3 ==== "
python3 sub-test3.py

echo " ==== Running sub-test4 ==== "
python3 sub-test4.py
