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
            sudo dnf -y install gcc-toolset-13 python3.12-devel python3.12-pip -y --skip-broken --nobest
            source /opt/rh/gcc-toolset-13/enable
        else
            sudo yum install gcc-toolset-13 python3.11-devel python3.11-pip -y
            source /opt/rh/gcc-toolset-13/enable
        fi
        ;;
    "ubuntu"|"debian")
        # Use: bash script.sh
        sudo apt update -y
        sudo apt install -y software-properties-common curl lsb-release gnupg2  libgomp1

        sudo add-apt-repository ppa:deadsnakes/ppa -y
        sudo apt update -y
        sudo apt update && apt install -y python3.12 python3.12-dev python3.12-venv python3-pip
        ;;
    "sles")
        sudo zypper refresh
        sudo zypper install -y gcc gcc-fortran python312 python312-pip python312-devel libjpeg62-devel gcc-c++ freetype2-devel
        sudo zypper install -y cargo cmake ncurses-devel gawk libopenssl-devel perl libgfortran5
        sudo zypper install -y zlib-devel libffi-devel readline-devel xz-devel sqlite3-devel libzip-devel bzip2 wget tar 
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

cd $WORKDIR

echo "Running example.py . . . ."
python3.12 ml_ds_example.py

echo "Running test . . . . ."
python3.12 sub-test1.py