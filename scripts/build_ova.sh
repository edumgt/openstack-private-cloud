#!/usr/bin/env bash
# build_ova.sh – VMware Workstation용 Ansible+OpenStack Lab VM 빌드 (Packer)
#
# 사전 요구 사항:
#   - VMware Workstation Pro 17  (https://www.vmware.com/products/workstation-pro.html)
#   - ovftool  (VMware OVF Tool – Workstation 설치 경로에 포함)
#     Windows: C:\Program Files (x86)\VMware\VMware Workstation\OVFTool\ovftool.exe
#     Linux:   /usr/bin/ovftool  또는  /usr/lib/vmware/ovftool/ovftool
#   - Packer >= 1.10  (https://developer.hashicorp.com/packer/install)
#
# 사용법:
#   ./scripts/build_ova.sh
#   ./scripts/build_ova.sh --only-validate   # 템플릿 문법 검사만 수행
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PACKER_DIR="${REPO_ROOT}/packer"
OUTPUT_DIR="${PACKER_DIR}/output-ansible-openstack-lab"
VM_NAME="ansible-openstack-lab"

##############################################################################
# 헬퍼
##############################################################################
info()  { echo "[INFO]  $*"; }
warn()  { echo "[WARN]  $*"; }
error() { echo "[ERROR] $*" >&2; exit 1; }

##############################################################################
# 의존성 확인
##############################################################################
command -v packer >/dev/null 2>&1 || error "packer not found. Install: https://developer.hashicorp.com/packer/install"

# ovftool 경로 탐색 (VMware Workstation 설치 위치별)
OVFTOOL=""
for candidate in \
    "ovftool" \
    "/usr/bin/ovftool" \
    "/usr/lib/vmware/ovftool/ovftool" \
    "/opt/vmware/ovftool/ovftool" \
    "C:/Program Files (x86)/VMware/VMware Workstation/OVFTool/ovftool.exe"; do
  if command -v "${candidate}" >/dev/null 2>&1; then
    OVFTOOL="${candidate}"
    break
  fi
done

info "Packer: $(packer version)"
if [ -n "${OVFTOOL}" ]; then
  info "ovftool: $(${OVFTOOL} --version 2>&1 | head -1)"
else
  warn "ovftool not found – OVA 변환을 건너뜁니다. VMX 파일로 직접 사용하세요."
fi

##############################################################################
# 검증만 수행
##############################################################################
if [[ "${1:-}" == "--only-validate" ]]; then
  info "Packer 플러그인 초기화..."
  packer init "${PACKER_DIR}"
  info "템플릿 문법 검사..."
  packer validate "${PACKER_DIR}"
  info "검증 통과."
  exit 0
fi

##############################################################################
# 빌드
##############################################################################
info "Packer 플러그인 초기화..."
packer init "${PACKER_DIR}"

info "VMware VM 빌드 시작 (ISO 다운로드 포함 시 약 30~60분 소요)..."
packer build -on-error=ask "${PACKER_DIR}"

##############################################################################
# VMX → OVA 변환 (ovftool 있는 경우)
##############################################################################
VMX_PATH="$(find "${OUTPUT_DIR}" -name "*.vmx" 2>/dev/null | head -1 || true)"
OVA_PATH="${OUTPUT_DIR}/${VM_NAME}.ova"

if [ -n "${OVFTOOL}" ] && [ -n "${VMX_PATH}" ] && [ -f "${VMX_PATH}" ]; then
  info "OVA 변환 중: ${VMX_PATH} → ${OVA_PATH}"
  "${OVFTOOL}" --acceptAllEulas --compress=9 "${VMX_PATH}" "${OVA_PATH}"
  info "OVA 빌드 완료: ${OVA_PATH}"
  info ""
  info "======================================================"
  info " VMware Workstation에서 OVA 열기:"
  info "   파일(File) → 열기(Open) → ${OVA_PATH}"
  info "======================================================"
else
  info "빌드 완료: ${OUTPUT_DIR}"
  info ""
  info "======================================================"
  info " VMware Workstation에서 VMX 직접 열기:"
  info "   파일(File) → 열기(Open) → ${VMX_PATH:-${OUTPUT_DIR}}"
  info ""
  info " OVA로 변환하려면 ovftool을 설치 후 아래 명령 실행:"
  info "   ovftool --acceptAllEulas <vm.vmx> ${VM_NAME}.ova"
  info "======================================================"
fi
