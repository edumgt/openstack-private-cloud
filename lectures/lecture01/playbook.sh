#!/bin/bash

# Ansible 학습환경 점검과 실행 루틴 정립

# Variables
LECTURE_ID="lecture01"
LECTURE_TITLE="Ansible 학습환경 점검과 실행 루틴 정립"
INSTALL_ENABLED="${INSTALL_ENABLED:-false}"
REFERENCE_PLAYBOOK="../../ansible/playbooks/00_ping.yml"
LECTURE_PACKAGES=(
    "python3"
    "python3-pip"
    "git"
    "curl"
    "jq"
)

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Show lecture context"
echo "=========================================="
echo "id=${LECTURE_ID}"
echo "title=${LECTURE_TITLE}"
echo "reference_playbook=${REFERENCE_PLAYBOOK}"
echo "install_enabled=${INSTALL_ENABLED}"
echo ""

# Install lecture packages when enabled
if [ "${INSTALL_ENABLED}" = "true" ]; then
    echo "Installing lecture packages..."
    
    # Detect package manager
    if command -v apt-get &> /dev/null; then
        PKG_MANAGER="apt-get"
        INSTALL_CMD="sudo apt-get install -y"
    elif command -v yum &> /dev/null; then
        PKG_MANAGER="yum"
        INSTALL_CMD="sudo yum install -y"
    elif command -v dnf &> /dev/null; then
        PKG_MANAGER="dnf"
        INSTALL_CMD="sudo dnf install -y"
    else
        echo -e "${RED}Error: No supported package manager found${NC}"
        exit 1
    fi
    
    echo "Using package manager: ${PKG_MANAGER}"
    
    for package in "${LECTURE_PACKAGES[@]}"; do
        echo "Installing ${package}..."
        ${INSTALL_CMD} ${package}
    done
    
    echo -e "${GREEN}Package installation completed${NC}"
else
    echo -e "${YELLOW}Package installation disabled (install_enabled=${INSTALL_ENABLED})${NC}"
fi

echo ""
echo "=========================================="
echo "Check Python3 availability"
echo "=========================================="

# Check Python3 availability
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo -e "${GREEN}Python3 is available${NC}"
    echo "python_version.stdout: ${PYTHON_VERSION}"
else
    echo -e "${RED}Python3 is not available${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Script completed successfully${NC}"
