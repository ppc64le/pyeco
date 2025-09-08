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
            dnf install -y python3-protobuf openblas openblas-devel python3.12-devel python3.12-pip
        else
            yum install -y python3-protobuf openblas openblas-devel python3.12-devel python3.12-pip
        fi
        ;;
    "ubuntu"|"debian")
        # Use: bash script.sh
        apt update &&  apt install -y \
        install python3-protobuf libopenblas-base libopenblas-dev python3.12 python3.12-dev python3.12-venv python3-pip
        ;;
    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac

yum 

apt 

python3.12 -m venv venv
source venv/bin/activate

pip install --no-cache --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux -r requirements.txt

# Exporting LD_LIBRARY_PATH for all the lib packages in requirements.txt
export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/abseilcpp/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/cares/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/ffmpeg/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/grpccpp/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/hdf5/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/lame/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/libprotobuf/lib64:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/libvpx/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/openblas/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/openmpi/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/opus/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/orc/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/re2/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/snappy/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/thriftcpp/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=./venv/lib64/python3.12/site-packages/utf8proc/lib:$LD_LIBRARY_PATH


python sub-test1.py
python sub-test2.py
python sub-test2.py



