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
            sudo dnf install -y python3.12 python3.12-devel python3.12-pip
        else
            sudo yum install -y python3.12 python3.12-devel python3.12-pip
        fi
        ;;
    "ubuntu"|"debian")
        # Use: bash script.sh
        export DEBIAN_FRONTEND=noninteractive
        sudo apt update && sudo apt install -y \
        python3.12 python3.12-dev python3.12-venv python3-pip \
        python3-protobuf 

        ;;
    "sles")
        # Enable necessary modules
        sudo zypper refresh
        sudo zypper install -y python312 python312-pip python312-devel

        ;;
    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac

# Create and activate virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install from requirements.txt with IBM ppc64le repository
pip install --prefer-binary --extra-index-url=https://py4power@ibm.com:eyJ2ZXIiOiIyIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYiLCJraWQiOiI1Z0dyZUE3SUk1NWNZelJDSmVHcDJXV01YSnV2SjJvWUNfeVcwNnM5WFQwIn0.eyJzdWIiOiJqZi1hY2Nlc3NAYzE0NTBhNDMtZjgyNS00MDA2LTg2ZjMtNDMzNzJiOTVmNjAxL3VzZXJzL3B5NHBvd2VyQGlibS5jb20iLCJzY3AiOiJhcHBsaWVkLXBlcm1pc3Npb25zL3VzZXIiLCJhdWQiOiIqQCoiLCJpc3MiOiJqZi1hY2Nlc3NAYzE0NTBhNDMtZjgyNS00MDA2LTg2ZjMtNDMzNzJiOTVmNjAxIiwiZXhwIjoxNzc1MDE5NjAxLCJpYXQiOjE3NjcyNDM2MDEsImp0aSI6ImJjYzdjOGUzLWE3NGQtNDRlOS05NTlhLTBlZjY3NmI3NzU0NCJ9.afs5nOH6ZYO10WYL2C1YirYM3A6WpDgfywtz2TvPG4MskMci6M7Oj9mvPARp316GdiVYFqZra9HzJ8XHr1jOZuxGH9uPoWjdEiaQq0krQsdT3fvz91CD80-MfMizrgwosoKFF70eEBO-vAPjhDWL_gJoGDpDCNzrx8dKlXkjB-jE5utJ5XZwYbFxKYgZYpm8ad1PuS4fheGCcvFA5G70PPDqN7pT_sWmNU_MIFnfRZADsru3331uZ4CoZMKYnuWKuTQD94N-Zb2sBLFb2NguerJ_brwz6uaVmpZALPVEQ6p92z3yu2dLPVjoGwlLq2XSPYW6UHujSdWGXhgp9Hm5_Q@na.artifactory.swg-devops.com/artifactory/api/pypi/sys-linux-power-team-pyeco-release-testing-pypi-local/simple -r requirements.txt

# Upgrade pip
pip install --upgrade pip

# Run Python scripts
echo "Running environment test..."
python3 dask_example.py

echo " ==== Running sub-test1 ==== "
python3 sub-test1.py

echo " ==== Running sub-test2 ==== "
python3 sub-test2.py
