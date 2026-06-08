################################################################################
# package-cp1.pkr.hcl
# 기존 VMware VM(cp1) → OVA 패키징 빌더
# 대상: 이미 OpenStack이 설치·구성된 cp1 VM을 배포 가능한 이미지로 추출
#
# 사용법:
#   ./scripts/package_vm.sh
#   또는 직접:
#   packer init packer/
#   packer build packer/package-cp1.pkr.hcl
################################################################################

packer {
  required_version = ">= 1.10.0"
  required_plugins {
    vmware = {
      version = ">= 1.0.11"
      source  = "github.com/hashicorp/vmware"
    }
  }
}

##############################################################################
# 변수
##############################################################################
variable "vm_name" {
  default = "openstack-aio-lab"
}

variable "source_vmx" {
  # WSL2에서 Windows 경로 접근
  default = "/mnt/c/Users/1/Documents/Virtual Machines/cp1/cp1.vmx"
}

variable "ssh_host" {
  default = "192.168.253.146"
}

variable "ssh_username" {
  default = "ubuntu"
}

variable "ssh_password" {
  default = "ubuntu"
}

variable "output_dir" {
  default = "output-openstack-aio"
}

##############################################################################
# Source – 기존 VMX 기반 빌드
##############################################################################
source "vmware-vmx" "cp1" {
  source_path = var.source_vmx

  # SSH 연결 (고정 IP 사용 – DHCP 대기 생략)
  communicator     = "ssh"
  ssh_host         = var.ssh_host
  ssh_username     = var.ssh_username
  ssh_password     = var.ssh_password
  ssh_timeout      = "15m"
  ssh_wait_timeout = "15m"

  # VM 종료 명령
  shutdown_command = "echo '${var.ssh_password}' | sudo -S shutdown -P now"
  shutdown_timeout = "5m"

  headless        = true
  linked          = false  # 독립 복사본 생성 (원본 보존)
  skip_compaction = false  # 디스크 압축 수행

  output_directory = "${path.root}/${var.output_dir}"
  vm_name          = var.vm_name
}

##############################################################################
# Build
##############################################################################
build {
  sources = ["source.vmware-vmx.cp1"]

  # ── 1. OpenStack 서비스 정지 & 시스템 정리 ──────────────────────
  provisioner "shell" {
    inline = [
      "sudo systemctl stop nova-compute nova-api nova-scheduler nova-conductor nova-novncproxy 2>/dev/null || true",
      "sudo systemctl stop neutron-server neutron-openvswitch-agent neutron-l3-agent neutron-dhcp-agent neutron-metadata-agent 2>/dev/null || true",
      "sudo systemctl stop glance-api cinder-api cinder-scheduler 2>/dev/null || true",
      "sudo systemctl stop apache2 2>/dev/null || true",
      "sudo find /var/log -type f -name '*.log' -exec truncate -s 0 {} \\;",
      "sudo find /var/log -type f -name '*.log.*' -delete",
      "sudo journalctl --rotate && sudo journalctl --vacuum-time=1s 2>/dev/null || true",
      "sudo find /var/lib/nova/instances -maxdepth 1 -mindepth 1 -type d -exec sudo rm -rf {} \\; 2>/dev/null || true",
      "sudo rm -f /root/.bash_history /home/ubuntu/.bash_history",
      "sudo rm -rf /tmp/* /var/tmp/*",
      "sudo cloud-init clean --logs 2>/dev/null || true",
      "sudo apt-get clean -y",
      "sudo dd if=/dev/zero of=/EMPTY bs=1M 2>/dev/null; sudo rm -f /EMPTY; sudo sync",
      "echo '=== 정리 완료 ==='"
    ]
  }

  # ── 2. OVA 내보내기 (ovftool 사용) ──────────────────────────────
  post-processor "shell-local" {
    inline = [
      "OVFTOOL='/mnt/c/Program Files (x86)/VMware/VMware Workstation/OVFTool/ovftool.exe'",
      "OUTPUT_VMX=$(find '${path.root}/${var.output_dir}' -name '*.vmx' | head -1)",
      "OVA_PATH='${path.root}/${var.output_dir}/${var.vm_name}.ova'",
      "echo '=== OVA 변환 시작 ==='",
      "\"$OVFTOOL\" --compress=9 --overwrite \"$OUTPUT_VMX\" \"$OVA_PATH\" && echo \"OVA 생성 완료: $OVA_PATH\""
    ]
  }
}
