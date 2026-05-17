# VMware Workstation 17 + Ubuntu 24.04 OpenStack 실습 환경 구성 가이드

이 문서는 VMware Workstation Pro 17에서 Ubuntu 24.04 Server VM을 생성하고,
DevStack 기반 OpenStack을 설치해 이 레포의 강의를 실행하는 전체 절차를 설명합니다.

---

## 1. 사전 요구 사항

| 항목 | 최소 | 권장 |
|---|---|---|
| VMware Workstation | Pro 17 | Pro 17.6.4+ |
| 호스트 RAM | 16 GB | **32 GB** |
| 호스트 디스크 여유 | 80 GB | 120 GB (SSD 권장) |
| 호스트 CPU | 4코어 (VT-x/AMD-V 활성화) | 8코어 이상 |
| Ubuntu ISO | ubuntu-24.04.x-live-server-amd64.iso | |
| WSL2 | Windows 11 | Windows 11 |

> VMware Workstation **Player**는 중첩 가상화(nested virtualization) 설정이 제한됩니다.
> OpenStack Nova Compute가 KVM을 사용하려면 **Pro** 버전이 필요합니다.

---

## 2. VMware Workstation 17 설치

`VMware-Workstation-Full-17.6.4-*.exe`를 실행해 설치합니다.

설치 후 BIOS/UEFI에서 가상화 기술이 활성화되어 있는지 확인합니다.

```powershell
# Windows PowerShell에서 확인
systeminfo | findstr /i "hyper-v\|virtualization"
```

---

## 3. Ubuntu 24.04 Server VM 생성

### 3.1 새 VM 마법사

VMware Workstation → **파일(File)** → **새 가상 머신(New Virtual Machine)**

| 단계 | 설정 값 |
|---|---|
| 설치 방법 | 나중에 OS 설치 (Installer disc image file 직접 지정) |
| 게스트 OS | Linux → **Ubuntu 64-bit** |
| VM 이름 | `ansible-openstack-lab` |
| 디스크 크기 | **80 GB** (단일 파일로 저장) |
| RAM | **16384 MB** (16 GB) |
| CPU | 프로세서 **4개**, 코어 **2개** (총 8 vCPU) |

### 3.2 중첩 가상화 활성화 (필수)

VM 설정 → **프로세서(Processors)** 탭:

```
☑ 이 가상 머신의 Intel VT-x/EPT 또는 AMD-V/RVI 가상화
  (Virtualize Intel VT-x/EPT or AMD-V/RVI)
```

이 옵션이 활성화되면 VM 내부에서 `/dev/kvm`이 노출됩니다.
DevStack의 Nova Compute가 실제 KVM 하이퍼바이저로 내부 VM을 구동합니다.

### 3.3 네트워크 어댑터 설정

VM 설정 → **네트워크 어댑터(Network Adapter)**:

```
● 브리지됨(Bridged): 물리 네트워크에 직접 연결
  ☑ 물리 네트워크 연결 복제(Replicate physical network connection state)
```

> **Bridged 모드를 사용하는 이유**: VM이 호스트 PC와 동일한 LAN IP 대역을 받아
> WSL2에서 VM IP로 직접 SSH 및 OpenStack API(5000번 포트 등) 접근이 가능합니다.
> NAT 모드는 WSL2 → Windows → VMware NAT 경로가 복잡해 권장하지 않습니다.

### 3.4 ISO 연결

VM 설정 → **CD/DVD (SATA)** → **ISO 이미지 파일 사용**:
```
ubuntu-24.04.4-live-server-amd64.iso 선택
```

---

## 4. Ubuntu 24.04 Server 설치

VM을 시작하면 Ubuntu 서버 설치 화면이 나타납니다.

### 4.1 주요 설치 옵션

| 항목 | 설정 |
|---|---|
| 언어 | English |
| 키보드 | 본인 환경에 맞게 |
| 네트워크 | DHCP 자동 할당 (Bridged이므로 LAN IP 받음) |
| 스토리지 | Use entire disk (LVM 없이) |
| 사용자 이름 | `ansible` |
| 비밀번호 | `ansible` |
| OpenSSH | **☑ Install OpenSSH server** |
| Featured snaps | 선택 없음 (DevStack이 직접 설치) |

### 4.2 설치 완료 후

재부팅 후 VM IP 확인:
```bash
ip addr show | grep "inet " | grep -v 127
# 예: inet 192.168.1.xxx/24
```

WSL2 또는 VMware 콘솔에서 SSH 접속:
```bash
ssh ansible@192.168.x.x   # 비밀번호: ansible
```

---

## 5. VM 기본 설정

```bash
# sudo 패스워드 없이 사용 가능하게 설정
echo "ansible ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/ansible

# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# KVM 사용 가능 여부 확인 (필수)
ls /dev/kvm && echo "KVM OK" || echo "KVM NOT FOUND - VM 프로세서 설정 확인 필요"

# 기본 도구 설치
sudo apt install -y python3 python3-pip python3-venv git curl net-tools
```

---

## 6. DevStack 설치 (OpenStack 실습 환경)

### 6.1 전제 패키지 설치

```bash
sudo apt install -y \
  git curl qemu-kvm libvirt-daemon-system libvirt-clients \
  bridge-utils python3-dev python3-venv \
  libffi-dev libssl-dev gcc make net-tools iptables
```

### 6.2 stack 유저 생성

```bash
sudo groupadd stack
sudo useradd -g stack -s /bin/bash -d /opt/devstack -m stack
echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/99-stack
sudo usermod -aG libvirt stack
```

### 6.3 DevStack 클론

```bash
sudo -iu stack git clone https://opendev.org/openstack/devstack \
  /opt/devstack/devstack -b stable/2024.2
```

### 6.4 local.conf 작성

```bash
HOST_IP=$(ip route get 1 | awk '{print $7; exit}')

sudo -iu stack tee /opt/devstack/devstack/local.conf << EOF
[[local|localrc]]
ADMIN_PASSWORD=123456
DATABASE_PASSWORD=123456
RABBIT_PASSWORD=123456
SERVICE_PASSWORD=123456
HOST_IP=${HOST_IP}
Q_AGENT=ovn
ENABLED_SERVICES=key,mysql,rabbit,etcd3,n-api,n-cpu,n-cond,n-sch,n-novnc,g-api,g-reg,q-svc,q-dhcp,q-ovn-metadata-agent,ovn-controller,ovn-northd,ovs-vswitchd,ovsdb-server,horizon,c-api,c-sch,c-vol,placement-api
LOGFILE=/opt/stack/logs/stack.sh.log
LOGDAYS=2
RECLONE=no
EOF
```

### 6.5 stack.sh 실행

```bash
sudo -iu stack bash -lc 'cd /opt/devstack/devstack && ./stack.sh'
# 약 20~40분 소요
```

설치 완료 확인:
```bash
HOST_IP=$(ip route get 1 | awk '{print $7; exit}')

# Keystone 응답 확인
curl http://${HOST_IP}:5000/v3

# Horizon 대시보드: 브라우저에서 http://<VM-IP>/dashboard
# 계정: admin / 123456
```

---

## 7. WSL2에서 Ansible 연결

WSL2 터미널에서 VM의 OpenStack을 제어합니다.

### 7.1 인벤토리 등록

SSH 키 등록 (권장):
```bash
# WSL2에서
ssh-keygen -t ed25519 -f ~/.ssh/vmware_openstack -N ""
ssh-copy-id -i ~/.ssh/vmware_openstack.pub ansible@192.168.x.x
```

```ini
# ansible/inventories/dev/hosts.ini
[openstack_hosts]
openstack1 ansible_host=192.168.x.x  ansible_user=ansible  ansible_ssh_private_key_file=~/.ssh/vmware_openstack
```

### 7.2 OpenStack openrc 파일 생성

```bash
# WSL2에서
mkdir -p .lab
cat > .lab/vmware-openrc << 'EOF'
export OS_AUTH_URL=http://192.168.x.x:5000/v3
export OS_USERNAME=admin
export OS_PASSWORD=123456
export OS_PROJECT_NAME=admin
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_DOMAIN_NAME=Default
export OS_REGION_NAME=RegionOne
export OS_IDENTITY_API_VERSION=3
EOF

source .lab/vmware-openrc
```

### 7.3 강의 실행

```bash
# lecture01 ~ lecture20: WSL2 localhost 대상 (기존과 동일)
ansible-playbook -i ansible/inventories/local/hosts.ini \
  lecture01/playbook.yml -e install_enabled=false

# lecture21: VMware VM의 OpenStack에 연결
source .lab/vmware-openrc
ansible-playbook -i ansible/inventories/local/hosts.ini \
  lecture21/playbook.yml \
  -e install_enabled=false \
  -e openrc_path=.lab/vmware-openrc

# lecture23 (Swift), lecture24 (Octavia): 동일하게 openrc_path 지정
ansible-playbook -i ansible/inventories/local/hosts.ini \
  lecture23/playbook.yml \
  -e install_enabled=false \
  -e openrc_path=.lab/vmware-openrc \
  -e use_mock_openstack_auth=false
```

---

## 8. Packer로 VM 이미지 자동 빌드 (선택)

이 레포의 `packer/ubuntu.pkr.hcl`은 VMware Workstation용 VM을 자동 빌드합니다.

```bash
# Packer 플러그인 초기화 (최초 1회)
packer init packer/

# 빌드 (약 30~60분)
./scripts/build_ova.sh
```

빌드 완료 후 VMware Workstation → **파일(File)** → **열기(Open)**로 VMX 또는 OVA 파일을 열어 사용합니다.

---

## 9. VM 스냅샷 활용

실습 중 환경이 망가졌을 때 빠르게 복구합니다.

```
VMware Workstation → VM 메뉴 → 스냅샷(Snapshot) → 스냅샷 찍기(Take Snapshot)
이름: "devstack-clean" → 확인
```

vmrun 명령어로도 가능:
```powershell
# Windows PowerShell
$vmrun = "C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe"
$vmx   = "C:\VMs\ansible-openstack-lab\ansible-openstack-lab.vmx"

# 스냅샷 생성
& $vmrun snapshot $vmx "devstack-clean"

# 스냅샷으로 복구
& $vmrun revertToSnapshot $vmx "devstack-clean"

# 스냅샷 목록
& $vmrun listSnapshots $vmx
```

---

## 10. 네트워크 모드 비교

| 모드 | VM IP | WSL2 접근 | 용도 |
|---|---|---|---|
| **Bridged** (권장) | LAN과 동일 대역 | 직접 접근 가능 | OpenStack 실습 |
| NAT | 192.168.x.x (VMware 가상) | 포트포워딩 필요 | 인터넷만 필요한 경우 |
| Host-Only | 192.168.x.x (호스트 전용) | 가능 (라우팅 필요) | 격리 테스트 |

### 폐쇄망 시뮬레이션 (Host-Only)

```
VM 설정 → 네트워크 어댑터 → Host-Only (VMnet1)
VMware 가상 네트워크 편집기 → VMnet1 → DHCP 설정 확인
```

폐쇄망 구성 상세: [airgap-config.md](./airgap-config.md)

---

## 11. 문제 해결

| 증상 | 원인 | 해결 방법 |
|---|---|---|
| `/dev/kvm` 없음 | VMware 프로세서 설정 미적용 | VM 설정 → 프로세서 → VT-x/AMD-V 중첩 가상화 체크 |
| SSH 접속 실패 | VM 아직 부팅 중 | 1분 대기 후 재시도 |
| `stack.sh` pip 오류 | Ubuntu 24.04 externally-managed | `sudo apt install -y python3-venv` 후 재시도 |
| WSL2에서 VM IP 미접근 | NAT 모드 사용 중 | 네트워크 어댑터를 Bridged로 변경 |
| DevStack 재설치 필요 | 환경 오염 | `cd /opt/devstack/devstack && ./unstack.sh && ./stack.sh` |
| Horizon 접속 불가 | Ubuntu 방화벽 | `sudo ufw disable` 또는 80 포트 허용 |
| `ansible` 명령 없음 | PATH 미설정 | `source ~/.bashrc` 또는 `.venv/bin/ansible` 사용 |
| Bridged 네트워크 IP 미할당 | VMware Bridged 어댑터 선택 오류 | VMware 가상 네트워크 편집기에서 Bridged 어댑터 재지정 |

## 유튜브 영상 찾아보기
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=vmware+workstation+ubuntu+24+openstack+devstack+ansible)
