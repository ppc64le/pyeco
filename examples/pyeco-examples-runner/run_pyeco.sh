#!/usr/bin/env bash
set -euo pipefail
#############################################
# Help and argument handling (NEW)
#############################################
usage() {
cat <<EOF
Usage: ./auto_new.sh [options] [selected_packages.txt]

Options:
  -h, --help        Show this help message and exit

Arguments:
  selected_packages.txt   Optional file with package names (one per line).
                          If not provided, ALL pyeco examples are run.

Behavior:
  - Python3.10 is ignored
  - Any error is reported as FAILED
  - Logs are classified into passed/ and failed/
  - XLS summary is generated at the end

Examples:
  ./auto_new.sh
  ./auto_new.sh selected_packages.txt
  ./auto_new.sh --help
EOF
}

# Handle --help before anything else
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    usage
    exit 0
fi

#############################################
# Original configuration (unchanged)
#############################################
REPO_URL="https://github.com/ppc64le/pyeco.git"
WORKDIR="/"
CLONE_DIR="${WORKDIR}/pyeco"
LOGS_DIR="${CLONE_DIR}/logs"

SELECTED_FILE="${1:-}"

RUN_TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RUN_DIR="pyeco_run_${RUN_TIMESTAMP}"
FINAL_LOG_DIR="${RUN_DIR}/logs"
PASSED_DIR="${FINAL_LOG_DIR}/passed"
FAILED_DIR="${FINAL_LOG_DIR}/failed"

mkdir -p "${PASSED_DIR}" "${FAILED_DIR}"

#############################################
# Wheel URL configuration (enhancement)
#############################################
BASE_WHEEL_URL="https://wheels.developerfirst.ibm.com/ppc64le/linux"
NEW_WHEEL_URL=""

if [ -t 0 ]; then
    echo "--------------------------------------------------"
    echo "Wheel URL Configuration"
    echo "--------------------------------------------------"
    echo "Default wheel URL:"
    echo "  ${BASE_WHEEL_URL}"
    read -r -p "Do you want to replace this URL? [y/N]: " ans
    ans="${ans:-n}"

    if [[ "$ans" =~ ^[Yy]$ ]]; then
        read -r -p "Enter new wheel URL: " NEW_WHEEL_URL
        if [ -z "${NEW_WHEEL_URL}" ]; then
            echo "ERROR: URL cannot be empty"
            exit 1
        fi
        echo "✔ Wheel URL will be replaced"
    else
        echo "✔ Keeping default wheel URL"
    fi
else
    echo "Non-interactive mode: skipping wheel URL prompt"
fi

#############################################
# Docker image definitions (unchanged)
#############################################
SLES_IMAGE="pyeco_sles_custom:latest"
SLES_DOCKERFILE="Dockerfile.sles"

UBUNTU_IMAGE="pyeco_ubuntu_custom:latest"
UBUNTU_DOCKERFILE="Dockerfile.ubuntu"

#############################################
# Build images (unchanged)
#############################################
docker build -t "${UBUNTU_IMAGE}" -f "${UBUNTU_DOCKERFILE}" .
docker build -t "${SLES_IMAGE}" -f "${SLES_DOCKERFILE}" .

#############################################
# Log classification (unchanged)
#############################################
classify_logs() {
    local temp_dir="$1"

    find "${temp_dir}/logs" -type f -name "*.log" | while read -r logfile; do
        if grep -q "^SUCCESS" "${logfile}" && ! grep -q "ERROR" "${logfile}"; then
            mv "${logfile}" "${PASSED_DIR}/"
        else
            mv "${logfile}" "${FAILED_DIR}/"
        fi
    done
}

#############################################
# Core container runner (UNCHANGED STRUCTURE)
#############################################
run_container() {
    local image="$1"
    local cname="$2"
    local platform="$3"

    TEMP_PLATFORM_DIR="${RUN_DIR}/tmp_${platform}"
    rm -rf "${TEMP_PLATFORM_DIR}"
    mkdir -p "${TEMP_PLATFORM_DIR}"

    docker rm -f "${cname}" >/dev/null 2>&1 || true
    docker run -d --name "${cname}" "${image}" sleep infinity

    if [[ "${platform}" == "ubuntu" ]]; then
        docker exec "${cname}" bash -c "apt update && apt install -y git sudo"
    elif [[ "${platform}" == "sles" ]]; then
        docker exec "${cname}" bash -c "zypper --non-interactive refresh && zypper --non-interactive install -y git sudo"
    else
        docker exec "${cname}" bash -c "yum install -y git sudo"
    fi

    if [ -n "${SELECTED_FILE}" ]; then
        docker cp "${SELECTED_FILE}" "${cname}:/tmp/selected_examples.txt"
    fi

    docker exec "${cname}" bash -c "
        rm -rf ${CLONE_DIR}
        git clone ${REPO_URL} ${CLONE_DIR}
        mkdir -p ${LOGS_DIR}
    "

    docker exec "${cname}" bash -c "
        set +e
        cd ${CLONE_DIR}/examples || exit 1

        should_skip_pyver() {
            [[ \"\$1\" == \"Python3.10\" ]]
        }

        run_pkg() {
            local pyver=\"\$1\"
            local pkg=\"\$2\"
            local pkg_dir=\"\$pyver/\$pkg\"
            local log=${LOGS_DIR}/${platform}_\${pyver}_\${pkg}.log

            echo \"Platform: ${platform}\" > \"\$log\"
            echo \"Python: \$pyver\" >> \"\$log\"
            echo \"Package: \$pkg\" >> \"\$log\"

            if [ -f \"\$pkg_dir/install_test_example.sh\" ]; then
                chmod +x \"\$pkg_dir/install_test_example.sh\"

                if [ -n \"${NEW_WHEEL_URL}\" ]; then
                    sed -i \"s|${BASE_WHEEL_URL}|${NEW_WHEEL_URL}|g\" \
                        \"\$pkg_dir/install_test_example.sh\" 2>/dev/null || true
                fi

                (cd \"\$pkg_dir\" && ./install_test_example.sh) >> \"\$log\" 2>&1
                rc=\$?
                if [ \$rc -eq 0 ]; then
                    echo \"SUCCESS\" >> \"\$log\"
                else
                    echo \"ERROR: exit \$rc\" >> \"\$log\"
                fi
            else
                echo \"ERROR: install_test_example.sh not found\" >> \"\$log\"
            fi
        }

        if [ -f /tmp/selected_examples.txt ]; then
            sed -i 's/\\r$//' /tmp/selected_examples.txt
            while read -r pkg_name; do
                pkg_name=\"\$(echo \"\$pkg_name\" | xargs)\"
                [ -z \"\$pkg_name\" ] && continue
                [[ \"\$pkg_name\" == \\#* ]] && continue

                for pyver in Python3.*; do
                    should_skip_pyver \"\$pyver\" && continue
                    match=\$(find \"\$pyver\" -maxdepth 1 -type d \
                        -iname \"*\${pkg_name}*\" -printf \"%f\\n\" | head -n 1)
                    [ -n \"\$match\" ] && run_pkg \"\$pyver\" \"\$match\"
                done
            done < /tmp/selected_examples.txt
        else
            for pyver in Python3.*; do
                should_skip_pyver \"\$pyver\" && continue
                for d in \"\$pyver\"/*; do
                    [ -d \"\$d\" ] || continue
                    run_pkg \"\$pyver\" \"\$(basename \"\$d\")\"
                done
            done
        fi
    "

    docker cp "${cname}:${LOGS_DIR}" "${TEMP_PLATFORM_DIR}"
    docker rm -f "${cname}" >/dev/null 2>&1 || true

    classify_logs "${TEMP_PLATFORM_DIR}"
    rm -rf "${TEMP_PLATFORM_DIR}"
}

#############################################
# Run all platforms (unchanged)
#############################################
run_container "registry.access.redhat.com/ubi9/ubi:9.6" "pyeco_ubi9" "ubi9"
run_container "${UBUNTU_IMAGE}" "pyeco_ubuntu" "ubuntu"
run_container "${SLES_IMAGE}" "pyeco_sles" "sles"

#############################################
# XLS summary (enhancement, read-only)
#############################################
SUMMARY_XLS="${RUN_DIR}/pyeco_summary.xlsx"

python3 <<EOF
from openpyxl import Workbook
from pathlib import Path

base = Path("${FINAL_LOG_DIR}")
wb = Workbook()
ws = wb.active
ws.title = "Summary"
ws.append(["Platform", "Python_Version", "Package", "Status", "Log_File"])

for status in ("passed", "failed"):
    for log in (base / status).glob("*.log"):
        parts = log.stem.split("_", 2)
        if len(parts) == 3:
            platform, python, pkg = parts
        else:
            platform = python = pkg = "UNKNOWN"
        ws.append([platform, python, pkg, status.upper(), log.name])

wb.save("${SUMMARY_XLS}")
EOF

echo "===================================================="
echo "Run completed"
echo "Logs:"
echo "  ${FINAL_LOG_DIR}/passed/"
echo "  ${FINAL_LOG_DIR}/failed/"
echo "XLS summary:"
echo "  ${SUMMARY_XLS}"
echo "===================================================="
