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

DISTRO=$(detect_distro)

case $DISTRO in
    "fedora"|"rhel"|"centos"|"rocky"|"almalinux")
        if command -v dnf >/dev/null 2>&1; then
            dnf install -y python3.12 python3.12-devel python3.12-pip
        else
            yum install -y python3.12 python3.12-devel python3.12-pip
        fi
        ;;
    "ubuntu"|"debian")
        export DEBIAN_FRONTEND=noninteractive
        apt update && apt install -y \
            python3.12 python3.12-dev python3.12-venv python3-pip
        ;;
    "sles")
        zypper refresh
        zypper install -y python312 python312-pip python312-devel
        ;;
    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac

# ----------------------------------------
# Python virtual environment
# ----------------------------------------
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip

pip install --no-cache --prefer-binary \
    --extra-index-url https://wheels.developerfirst.ibm.com/ppc64le/linux-v2026.03.31 \
    -r requirements.txt

# ----------------------------------------
# Add ollama binary to PATH
# ----------------------------------------
OLLAMA_BIN=$(find venv -name "ollama" -type f | head -1 | xargs dirname)
export PATH="$PATH:$OLLAMA_BIN"
echo "Ollama binary path: $OLLAMA_BIN"
echo "Ollama version: $(ollama --version)"

# ----------------------------------------
# Start Ollama server if not running
# ----------------------------------------
if curl -s http://localhost:11434 > /dev/null 2>&1; then
    echo "[INFO] Ollama server already running"
else
    echo "[INFO] Starting Ollama server..."
    ollama serve > /tmp/ollama.log 2>&1 &
    sleep 4
    echo "[INFO] Ollama server started"
fi

# Pull model
echo "[INFO] Pulling tinyllama model..."
ollama pull tinyllama

# ----------------------------------------
# Run scripts
# ----------------------------------------
echo ""
echo "==== Running ollama_example.py ===="
python ollama_example.py

echo ""
echo "==== Running sub-test1.py ===="
python sub-test1.py

echo ""
echo "==== Running sub-test2.py ===="
python sub-test2.py
