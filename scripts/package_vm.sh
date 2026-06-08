#!/bin/bash
# OpenStack AIO VM 패키징 스크립트
# cp1 VMware VM → OVA 패키지
#
# 사용법: ./scripts/package_vm.sh [output_dir]
# 예시:  ./scripts/package_vm.sh /tmp/openstack-package

set -euo pipefail

##############################################################################
# 설정
##############################################################################
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

VM_NAME="openstack-aio-lab"
SOURCE_VMX="/mnt/c/Users/1/Documents/Virtual Machines/cp1/cp1.vmx"
VM_HOST="192.168.253.146"
VM_USER="ubuntu"
VM_PASS="ubuntu"

VMRUN="/mnt/c/Program Files (x86)/VMware/VMware Workstation/vmrun.exe"
OVFTOOL="/mnt/c/Program Files (x86)/VMware/VMware Workstation/OVFTool/ovftool.exe"
PACKER_HCL="$REPO_ROOT/packer/package-cp1.pkr.hcl"

OUTPUT_DIR="${1:-$REPO_ROOT/packer/output-openstack-aio}"
OVA_PATH="$OUTPUT_DIR/${VM_NAME}.ova"

##############################################################################
# 색상 출력
##############################################################################
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
info() { echo -e "${CYAN}[>>]${NC} $1"; }
warn() { echo -e "${YELLOW}[!!]${NC} $1"; }
err()  { echo -e "${RED}[ERR]${NC} $1"; exit 1; }

##############################################################################
# 사전 검사
##############################################################################
echo "========================================"
echo "  OpenStack AIO VM Packager"
echo "========================================"

info "사전 조건 확인..."

[ -f "$SOURCE_VMX" ]  || err "VMX 파일 없음: $SOURCE_VMX"
[ -f "$VMRUN" ]       || err "vmrun.exe 없음: $VMRUN"
[ -f "$OVFTOOL" ]     || err "ovftool.exe 없음: $OVFTOOL"
command -v packer &>/dev/null || err "packer 명령어 없음. https://developer.hashicorp.com/packer/install 참고"
command -v sshpass &>/dev/null || { warn "sshpass 없음. 설치 중..."; sudo apt-get install -y sshpass -q; }

ok "사전 조건 확인 완료"

##############################################################################
# VM 상태 확인
##############################################################################
info "VM 전원 상태 확인..."
VM_STATE=$("$VMRUN" list 2>/dev/null | grep -c "cp1.vmx" || true)

if [ "$VM_STATE" -gt 0 ]; then
  info "VM이 실행 중입니다. Packer를 통해 정리 후 종료합니다."
  BUILD_MODE="packer"
else
  info "VM이 꺼진 상태입니다. ovftool로 직접 OVA를 생성합니다."
  BUILD_MODE="ovftool"
fi

##############################################################################
# 모드 1: VM 실행 중 → Packer로 정리 + 종료 + 내보내기
##############################################################################
if [ "$BUILD_MODE" = "packer" ]; then
  info "Packer 플러그인 초기화..."
  cd "$REPO_ROOT/packer"
  packer init package-cp1.pkr.hcl

  info "Packer 빌드 시작 (정리 → 종료 → OVA 내보내기)..."
  packer build \
    -var "output_dir=$(basename "$OUTPUT_DIR")" \
    -var "vm_name=$VM_NAME" \
    package-cp1.pkr.hcl

  ok "Packer 빌드 완료"

##############################################################################
# 모드 2: VM 꺼진 상태 → ovftool로 직접 OVA 생성
##############################################################################
else
  mkdir -p "$OUTPUT_DIR"

  info "ovftool로 OVA 내보내기 시작..."
  info "  소스: $SOURCE_VMX"
  info "  출력: $OVA_PATH"

  # Windows 경로로 변환 (ovftool.exe는 Windows 경로 필요)
  WIN_SOURCE=$(wslpath -w "$SOURCE_VMX")
  WIN_OUTPUT=$(wslpath -w "$OVA_PATH")

  "$OVFTOOL" \
    --compress=9 \
    --overwrite \
    --diskMode=thin \
    --exportFlags=preserveIdentity \
    "$WIN_SOURCE" \
    "$WIN_OUTPUT"

  ok "OVA 내보내기 완료"
fi

##############################################################################
# 결과 출력
##############################################################################
echo ""
echo "========================================"
echo "  패키징 완료"
echo "========================================"
if [ -f "$OVA_PATH" ]; then
  OVA_SIZE=$(du -sh "$OVA_PATH" | cut -f1)
  ok "OVA 파일: $OVA_PATH ($OVA_SIZE)"
  echo ""
  echo "  VMware에서 가져오기:"
  echo "    File → Open → $(wslpath -w "$OVA_PATH" 2>/dev/null || echo "$OVA_PATH")"
  echo ""
  echo "  기본 접속 정보:"
  echo "    SSH: ssh ubuntu@<VM_IP>  (pw: ubuntu)"
  echo "    Horizon: http://<VM_IP>/dashboard  (admin / openstack)"
else
  warn "OVA 파일을 찾을 수 없습니다: $OVA_PATH"
  info "packer/output-openstack-aio/ 디렉토리 확인:"
  ls -lh "$OUTPUT_DIR/" 2>/dev/null || true
fi
