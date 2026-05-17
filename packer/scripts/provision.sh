#!/usr/bin/env bash
# provision.sh – VM 내부 핵심 프로비저닝 (root 권한으로 실행)
# Ubuntu 24.04 LTS (Noble) 기준
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

ANSIBLE_USER="${ANSIBLE_USER:-ansible}"
WORKSPACE="/opt/ansible-openstack"

echo "==> [provision] 패키지 업데이트 및 설치"
apt-get update -y
apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    python3-full \
    git \
    curl \
    wget \
    ca-certificates \
    gnupg \
    lsb-release \
    apt-transport-https \
    software-properties-common \
    vim \
    net-tools \
    openssh-server \
    unzip \
    jq

echo "==> [provision] Python venv 생성 (Ubuntu 24.04 externally-managed 대응)"
python3 -m venv /opt/venv
# shellcheck disable=SC1091
source /opt/venv/bin/activate

echo "==> [provision] pip 업그레이드"
pip install --upgrade pip

echo "==> [provision] ansible-core 및 필수 라이브러리 설치"
pip install \
    "ansible-core>=2.16" \
    ansible-lint \
    boto3 \
    botocore \
    openstacksdk \
    python-openstackclient

deactivate

echo "==> [provision] 심볼릭 링크 (PATH에서 직접 사용 가능하도록)"
ln -sf /opt/venv/bin/ansible          /usr/local/bin/ansible
ln -sf /opt/venv/bin/ansible-playbook /usr/local/bin/ansible-playbook
ln -sf /opt/venv/bin/ansible-galaxy   /usr/local/bin/ansible-galaxy
ln -sf /opt/venv/bin/openstack        /usr/local/bin/openstack

echo "==> [provision] 워크스페이스 디렉토리 생성"
mkdir -p "${WORKSPACE}"
chown -R "${ANSIBLE_USER}:${ANSIBLE_USER}" "${WORKSPACE}"

echo "==> [provision] 사용자 쉘 환경 설정"
cat >> /home/"${ANSIBLE_USER}"/.bashrc << 'EOF'

# Ansible OpenStack Lab
export WORKSPACE=/opt/ansible-openstack
export PATH="/opt/venv/bin:$PATH"
alias cdlab='cd $WORKSPACE'
alias ap='ansible-playbook'
EOF

echo "==> [provision] 완료."
