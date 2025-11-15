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
            sudo dnf install gcc-toolset-13 python3.12-devel python3.12-pip openblas openblas-devel protobuf protobuf-devel libjpeg-turbo-devel wget krb5-devel gcc python3-devel gcc-gfortran -y --skip-broken --nobest
            sudo dnf install -y gcc gcc-c++ gcc-gfortran git wget xz cmake make yum-utils sudo llvm
            sudo dnf config-manager --add-repo https://mirror.stream.centos.org/9-stream/AppStream/ppc64le/os/
            sudo dnf config-manager --add-repo https://mirror.stream.centos.org/9-stream/BaseOS/ppc64le/os/
            sudo dnf config-manager --add-repo https://mirror.stream.centos.org/9-stream/CRB/ppc64le/os/

            sudo wget http://mirror.centos.org/centos/RPM-GPG-KEY-CentOS-Official
            sudo mv RPM-GPG-KEY-CentOS-Official /etc/pki/rpm-gpg/.
            sudo rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-Official

            sudo dnf install --nodocs -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
            sudo dnf -y install  proj proj-devel
            source /opt/rh/gcc-toolset-13/enable
        else
            sudo yum install gcc-toolset-13 python3.11-devel python3.11-pip -y
            source /opt/rh/gcc-toolset-13/enable
        fi
        ;;
    "ubuntu"|"debian")
        sudo apt update -y
        sudo apt install -y software-properties-common curl lsb-release gnupg2  libgomp1 gfortran libkrb5-dev krb5-user build-essential python3.12-dev python3.12-venv libopenblas-dev libjpeg-dev zlib1g-dev pkg-config libjpeg62
        sudo add-apt-repository ppa:deadsnakes/ppa -y
        sudo apt update -y
        sudo apt update && apt install -y python3.12 python3.12-dev python3.12-venv python3-pip
        ;;
    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac



python3.12 -m venv .venv
source .venv/bin/activate

python3.12 -m pip install --no-cache --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux -r requirements.txt

WORKDIR=$(pwd)

SITE_PACKAGES=$(python -c "import sysconfig; print(sysconfig.get_paths()['purelib'])")

export LD_LIBRARY_PATH=./.venv/lib64/python3.12/site-packages/libprotobuf/lib64:$LD_LIBRARY_PATH

# Check for openblas folder in site-packages or system
OPENBLAS_DIR=$(find "$SITE_PACKAGES" /usr -type f -name "libopenblas.so*" 2>/dev/null | head -n1 | xargs dirname)

if [ -n "$OPENBLAS_DIR" ]; then
    export LD_LIBRARY_PATH="$OPENBLAS_DIR:$LD_LIBRARY_PATH"
else
    echo "Warning: libopenblas.so not found, please install OpenBLAS."
fi

cd $WORKDIR

echo "Running example.py . . . ."
python3.12 example.py

echo "Running test . . . . ."
python3.12 test.py