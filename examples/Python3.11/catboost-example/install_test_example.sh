#!/bin/bash
set -e

echo "========== START: CatBoost Example Setup =========="

# -------------------------------
# Detect OS
# -------------------------------
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo $ID
    else
        echo "unknown"
    fi
}

DISTRO=$(detect_distro)

if [ "$EUID" -eq 0 ]; then
    SUDO=""
else
    SUDO="sudo"
fi

# -------------------------------
# Install system dependencies
# -------------------------------
echo "========== Installing system dependencies =========="

case $DISTRO in
    "fedora"|"rhel"|"centos"|"rocky"|"almalinux")
        $SUDO dnf install -y python3.12 python3.12-devel python3.12-pip gcc gcc-c++ make
        ;;
    "ubuntu"|"debian")
        $SUDO apt update
        $SUDO apt install -y python3.12 python3.12-dev python3.12-venv python3-pip build-essential
        ;;
    *)
        echo " Unsupported distro: $DISTRO"
        exit 1
        ;;
esac

# -------------------------------
# Create venv
# -------------------------------
echo "========== Creating virtual environment =========="

python3.12 -m venv .venv
source .venv/bin/activate

python --version

# -------------------------------
# Upgrade pip
# -------------------------------
echo "========== Upgrading pip =========="

pip install --upgrade pip setuptools wheel

# -------------------------------
# Install base deps
# -------------------------------
echo "========== Installing base dependencies =========="

pip install --no-cache --prefer-binary --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux -r requirements.txt


# -------------------------------
# Install CatBoost (STRICT)
# -------------------------------
echo "========== Installing CatBoost =========="

if ! pip install --prefer-binary --no-cache catboost; then
    echo ""
    echo " CatBoost installation FAILED"
    echo " Reason: No prebuilt wheel available (ppc64le)"
    echo " Source build is intentionally NOT allowed (unstable)"
    echo ""
    echo " ACTION REQUIRED:"
    echo "   - Upload CatBoost wheel to IBM repo OR JFrog"
    echo "   - OR install from internal repository"
    echo ""
    exit 1
fi

# -------------------------------
# Verify installation
# -------------------------------
echo "========== Verifying CatBoost =========="

python - <<EOF
import catboost
print("✅ CatBoost version:", catboost.__version__)
EOF

# -------------------------------
# Run tests
# -------------------------------
echo "========== Running tests =========="

python catboost_example.py
python sub-test1.py
echo "Test-1 passed"
python sub-test2.py
echo "Test-2 passed"
python sub-test3.py
echo "Test-3 passed"

echo "ALL TESTS PASSED SUCCESSFULLY"
