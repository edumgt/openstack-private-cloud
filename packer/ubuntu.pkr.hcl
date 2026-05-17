################################################################################
# ubuntu.pkr.hcl
# VMware Workstation VMDK 빌더 – Ubuntu 24.04 LTS
# Packer >= 1.10 (HCL2)
#
# 사전 요구 사항:
#   - VMware Workstation Pro 17
#   - ovftool (OVA 변환 시, VMware Workstation 설치 경로에 포함)
#   - Packer >= 1.10  (https://developer.hashicorp.com/packer/install)
#
# 사용법:
#   packer init   packer/
#   packer build  packer/
#
# 빌드 결과물: packer/output-ansible-openstack-lab/
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
# 변수 – -var 'key=value' 또는 packer.auto.pkrvars.hcl 로 오버라이드
##############################################################################
variable "vm_name" {
  default = "ansible-openstack-lab"
}

variable "vm_memory_mb" {
  # DevStack 최소 8 GB, 권장 16 GB
  default = "16384"
}

variable "vm_cpus" {
  default = "4"
}

variable "disk_size_mb" {
  # 80 GB
  default = "81920"
}

variable "iso_url" {
  # Ubuntu 24.04 LTS (Noble) server ISO
  # 로컬 ISO 경로 예: "iso/ubuntu-24.04.4-live-server-amd64.iso"
  # 온라인: "https://releases.ubuntu.com/24.04/ubuntu-24.04.4-live-server-amd64.iso"
  default = "iso/ubuntu-24.04.4-live-server-amd64.iso"
}

variable "iso_checksum" {
  # sha256 체크섬 – Ubuntu 공식 릴리스 페이지에서 확인
  # https://releases.ubuntu.com/24.04/SHA256SUMS
  default = "none"
}

variable "ssh_username" {
  default = "ansible"
}

variable "ssh_password" {
  default = "ansible"
}

##############################################################################
# Source – VMware Workstation ISO 부트
##############################################################################
source "vmware-iso" "ubuntu" {
  vm_name       = var.vm_name
  guest_os_type = "ubuntu-64"
  memory        = var.vm_memory_mb
  cpus          = var.vm_cpus
  disk_size     = var.disk_size_mb
  disk_type_id  = 0

  iso_url      = var.iso_url
  iso_checksum = var.iso_checksum

  # Ubuntu 24.04 live-server: subiquity / cloud-init autoinstall
  http_directory = "${path.root}/http"
  boot_wait      = "5s"
  boot_command = [
    "c<wait>",
    "linux /casper/vmlinuz --- autoinstall ds=nocloud-net;seedfrom=http://{{ .HTTPIP }}:{{ .HTTPPort }}/<wait>",
    "<enter><wait>",
    "initrd /casper/initrd<wait>",
    "<enter><wait>",
    "boot<enter>"
  ]

  shutdown_command = "echo '${var.ssh_password}' | sudo -S shutdown -P now"

  communicator           = "ssh"
  ssh_username           = var.ssh_username
  ssh_password           = var.ssh_password
  ssh_timeout            = "40m"
  ssh_handshake_attempts = 150

  # VMware Workstation 17 하드웨어 버전
  version = "20"

  # 네트워크: Bridged (WSL2 직접 접근용)
  network              = "bridged"
  network_adapter_type = "vmxnet3"

  # VMware 전용 설정
  vmx_data = {
    # 중첩 가상화 활성화 – Nova Compute KVM 사용에 필수
    "vhv.enable"              = "TRUE"
    "vpmc.enable"             = "TRUE"
    # 불필요한 하드웨어 비활성화 (VM 크기/속도 최적화)
    "sound.present"           = "FALSE"
    "usb.present"             = "FALSE"
    "mks.enable3d"            = "FALSE"
    "disk.EnableUUID"         = "TRUE"
    "tools.syncTime"          = "TRUE"
    "ethernet0.pcislotnumber" = "32"
  }

  output_directory = "${path.root}/output-${var.vm_name}"
  skip_compaction  = false
  headless         = true
}

##############################################################################
# Build
##############################################################################
build {
  sources = ["source.vmware-iso.ubuntu"]

  # 1. cloud-init 완료 대기
  provisioner "shell" {
    inline = [
      "sudo cloud-init status --wait || true"
    ]
    pause_before = "10s"
  }

  # 2. 핵심 프로비저닝: Python, Ansible, 도구 설치
  provisioner "shell" {
    script          = "${path.root}/scripts/provision.sh"
    execute_command = "echo '${var.ssh_password}' | sudo -S bash '{{.Path}}'"
    environment_vars = [
      "ANSIBLE_USER=${var.ssh_username}"
    ]
  }

  # 3. 레포 콘텐츠 VM에 복사
  provisioner "file" {
    source      = "${path.root}/../"
    destination = "/opt/ansible-openstack"
    generated   = false
  }

  # 4. 복사 후 설정 (소유권, 오프라인 pip wheel 캐시)
  provisioner "shell" {
    script          = "${path.root}/scripts/post_copy.sh"
    execute_command = "echo '${var.ssh_password}' | sudo -S bash '{{.Path}}'"
    environment_vars = [
      "ANSIBLE_USER=${var.ssh_username}"
    ]
  }

  # 5. 정리 (VM 크기 축소)
  provisioner "shell" {
    script          = "${path.root}/scripts/cleanup.sh"
    execute_command = "echo '${var.ssh_password}' | sudo -S bash '{{.Path}}'"
  }
}
