# Python Ansible 기반 Openstack Private Cloud 운영

## 1. 학습 목표
- Ansible 플레이북 작성/실행/검증 루틴을 익힌다.
- 인벤토리, 변수, 템플릿, Role을 재사용 가능한 형태로 설계한다.
- 서비스 운영 자동화(Nginx, Docker)를 안정적으로 수행한다.
- OpenStack 핵심 컴포넌트(Keystone/Glance/Nova/Neutron/Cinder) 운영 흐름을 Ansible 관점으로 이해한다.
- 마지막 강의에서 운영 Runbook을 완성해 재현 가능한 실습 체계를 만든다.

## 2. 통합 기술 스택 가이드
### 핵심 스택
- `ansible-core`, `yaml`, `python3`, `linux`, `openstack`

### 보조 스택
- `docker`, `nginx`, `awscli`, `az` (비교 학습 목적)

### OpenStack 컴포넌트 정리 (기술스택 문서 병합 요약)
- `Keystone`: 인증/권한/서비스 카탈로그 (Python)
- `Glance`: VM 이미지 관리 (Python)
- `Nova`: 인스턴스 생성/스케줄링/컴퓨트 제어 (Python)
- `Neutron`: 네트워크/서브넷/라우터/FIP 제어 (Python)
- `Cinder`: 블록 스토리지 볼륨/스냅샷 관리 (Python)
- `Horizon`: Django 기반 웹 대시보드 (Python + HTML/CSS/JS)

## 3. 20강 로드맵
| Lecture | 모듈 | 주제 |
|---|---|---|
| lecture01 | Ansible Foundation | Ansible 학습환경 점검과 실행 루틴 정립 |
| lecture02 | Ansible Foundation | Inventory/Variables 구조 설계 |
| lecture03 | Ansible Foundation | Ad-hoc 명령과 Facts 수집 자동화 |
| lecture04 | Ansible Foundation | Jinja2 템플릿과 Handler 실전 |
| lecture05 | Ansible Foundation | Role 분리와 재사용 설계 |
| lecture06 | Ansible Foundation | Idempotency와 검증 자동화 |
| lecture07 | Ansible Operations | 사용자/권한/SSH 정책 자동화 |
| lecture08 | Ansible Operations | Nginx 서비스 배포와 검증 |
| lecture09 | Ansible Operations | Docker Engine 설치 자동화 |
| lecture10 | Ansible Operations | Compose 배포와 업데이트 전략 |
| lecture11 | OpenStack Foundation | OpenStack CLI 환경 구성과 인증 토큰 흐름 |
| lecture12 | OpenStack Foundation | OpenStack 프로젝트/네트워크 리소스 자동화 기초 |
| lecture13 | OpenStack Foundation | OpenStack 아키텍처와 핵심 서비스 이해 |
| lecture14 | OpenStack Foundation | Keystone 인증/프로젝트/역할 모델 |
| lecture15 | OpenStack Foundation | Glance 이미지 관리 자동화 |
| lecture16 | OpenStack Foundation | Nova 인스턴스 라이프사이클 자동화 |
| lecture17 | OpenStack Foundation | Neutron/Cinder 리소스 자동화 |
| lecture18 | OpenStack Operations | Horizon 운영 점검과 로그 수집 |
| lecture19 | OpenStack Operations | Kolla Ansible 배포 준비와 검증 |
| lecture20 | OpenStack Operations | 종합 캡스톤: OpenStack 운영 Runbook 완성 |

## 4. 주차별 학습 계획 (압축판)
- Week 1: `lecture01~05` (기초 문법/구조)
- Week 2: `lecture06~10` (운영 자동화)
- Week 3: `lecture11~15` (OpenStack Foundation)
- Week 4: `lecture16~20` (OpenStack 운영/캡스톤)

권장 학습 시간: 강의당 60~90분

## 5. 실행 방법 (상세)
### 5.1 사전 준비
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install ansible-core
ansible --version
```

### 5.2 강의 실행 템플릿
```bash
# 기본 실행 (설치 태스크 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lectureNN/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lectureNN/playbook.yml -e install_enabled=true
```

### 5.3 예시 (lecture01)
```bash
ansible-playbook -i ansible/inventories/local/hosts.ini lecture01/playbook.yml -e install_enabled=false
ansible-playbook -i ansible/inventories/local/hosts.ini lecture01/playbook.yml -e install_enabled=true
```

### 5.4 레퍼런스 플레이북 실행
각 강의의 `lecture.yml`에 있는 `ansible_lab.reference_playbook`을 참고해 아래처럼 실행합니다.
```bash
ansible-playbook -i ansible/inventories/local/hosts.ini ansible/playbooks/00_ping.yml
```

## 6. 결과 검증 체크리스트
강의마다 아래 4가지를 남기면 재현성이 높아집니다.
- 실행 로그 1개
- 핵심 태스크 성공/실패 원인 정리 1개
- 개선 포인트 1개
- 다음 강의 연결 메모 1개

## 7. 프로젝트 구조 (개편 후)
```text
Python_Ansible-Playbook/
├── README.md
├── lecture01/
├── lecture02/
├── ...
├── lecture20/
├── ansible/
│   ├── inventories/
│   ├── playbooks/
│   ├── roles/
│   ├── group_vars/
│   ├── files/
│   └── stacks/
├── docs/
│   └── reference/
├── scripts/
└── archive/
    └── legacy/
```

## 8. 운영 메모
- `install_enabled=true` 검증 시 OS 저장소 패키지명 차이로 실패할 수 있습니다.
- 클라우드 실습(OpenStack/AWS/Azure 비교)은 로컬 패키지 설치와 별도로 자격증명/네트워크가 필요합니다.
- 실패 로그를 남기고 `README`의 트러블슈팅 섹션과 함께 비교하면 학습 속도가 빨라집니다.

## 9. 클라우드 자동화 조합 설명 및 비교
### 9.1 조합 설명
- `OpenStack + Ansible`: 운영자가 원하는 상태를 playbook으로 선언하고, 여러 OpenStack 리소스를 반복 가능하게 표준화할 때 유리합니다.
- `AWS + aws cli`: AWS 서비스별 API를 즉시 호출해 빠르게 스크립트화하거나 CI에서 단일 작업을 제어할 때 유리합니다.
- `Azure + az`: Azure 리소스 그룹/구독 단위 운영을 CLI 중심으로 자동화하고 파이프라인과 연동할 때 유리합니다.

### 9.2 비교표
| 조합 | 자동화 방식 | 강점 | 약점 | 적합한 상황 |
|---|---|---|---|---|
| OpenStack + Ansible | 선언형(playbook, role) | 일관성, 재실행 안정성, 팀 표준화 | 초기 구조 설계 비용 | 사내 프라이빗 클라우드 운영 표준화 |
| AWS + aws cli | 명령형(스크립트/파이프라인) | 빠른 실험, 서비스 기능 접근 속도 | 스크립트가 커지면 유지보수 부담 | AWS 관리 작업의 빠른 자동화 |
| Azure + az | 명령형(스크립트/파이프라인) | 구독/리소스그룹 단위 관리가 직관적 | 대규모 반복 작업은 구조화 필요 | Azure 운영팀의 일상 작업 자동화 |

### 9.3 최소 예시 명령
```bash
# OpenStack + Ansible
ansible-playbook -i ansible/inventories/local/hosts.ini lecture13/playbook.yml -e install_enabled=false

# AWS + aws cli
aws ec2 describe-instances --region ap-northeast-2

# Azure + az
az vm list -o table
```

### 9.4 OpenStack 리소스와 AWS 대응 리소스 설명
이 저장소의 강의/플레이북 흐름 기준으로, 아래처럼 OpenStack 리소스를 AWS 리소스와 1:1에 가깝게 비교해 학습할 수 있습니다.

| OpenStack 리소스 | AWS 대응 리소스 | 핵심 설명 | 이 저장소에서 연결되는 학습 지점 |
|---|---|---|---|
| Keystone (User/Project/Role) | IAM (User/Group/Role/Policy) | 인증/권한 관리 계층. Keystone은 프로젝트(tenant) 중심, AWS는 계정/정책 중심으로 접근합니다. | `lecture14/README.md`, `lecture14/lecture.yml` |
| Neutron Network/Subnet/Router/SG/FIP | VPC/Subnet/Route Table/SG/Elastic IP | 가상 네트워크 구성 요소. 라우팅/보안그룹/공인 IP를 각각 대응해 이해하면 운영 모델 전환이 쉬워집니다. | `lecture12/README.md`, `lecture17/README.md`, `ansible/playbooks/20_aws_create_vpc.yml` |
| Nova Instance | EC2 Instance | 가상머신 컴퓨트 리소스. 생성/삭제/상태 점검/접속 자동화 흐름이 유사합니다. | `lecture16/README.md`, `ansible/playbooks/21_aws_create_ec2.yml` |
| Glance Image | AMI | 인스턴스 생성용 베이스 이미지 저장소. 이미지 버전/공유 정책 관리가 핵심입니다. | `lecture15/README.md` |
| Cinder Volume/Snapshot | EBS Volume/Snapshot | 블록 스토리지. 인스턴스 연결/분리, 스냅샷 기반 백업/복구 흐름이 동일한 운영 패턴을 가집니다. | `lecture17/README.md` |
| Swift Object Storage | S3 | 오브젝트 스토리지. 버킷/컨테이너, 객체 업로드/수명주기/접근정책 관점에서 비교 가능합니다. | `lecture23/README.md`, `ansible/playbooks/22_aws_s3_bucket.yml` |
| Horizon Dashboard | AWS Management Console | 웹 UI 기반 운영 콘솔. CLI/Ansible 자동화와 병행해 상태 확인/운영 점검에 사용합니다. | `lecture18/README.md` |

## 10. GitHub Actions: Docker Hub Push + Local Docker Sync
### 10.1 추가된 파일
- `.github/workflows/docker-publish.yml`
- `Dockerfile`
- `.dockerignore`
- `scripts/sync_local_docker.sh`

### 10.2 GitHub Secrets (필수)
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN` (Docker Hub Access Token)

### 10.3 GitHub Variables (선택)
- `DOCKERHUB_REPOSITORY`: 미설정 시 `python-ansible-playbook`
- `ENABLE_LOCAL_DOCKER_SYNC`: `true`일 때 self-hosted runner에서 local docker 반영
- `LOCAL_DOCKER_CONTAINER_NAME`: 미설정 시 `python-ansible-playbook`
- `LOCAL_DOCKER_RUN_CMD`: 미설정 시 `tail -f /dev/null`

### 10.4 동작 방식
1. `main` 브랜치 push(또는 수동 실행) 시 Docker 이미지를 빌드해 Docker Hub로 push
2. `ENABLE_LOCAL_DOCKER_SYNC=true`이고 self-hosted runner(`self-hosted`, `linux`, `docker`)가 있으면
   같은 워크플로우에서 최신 이미지를 pull하고 로컬 컨테이너를 재기동

### 10.5 수동 로컬 반영 (원할 때 직접 실행)
```bash
IMAGE=docker.io/<dockerhub-user>/<repo>:latest \
CONTAINER_NAME=python-ansible-playbook \
./scripts/sync_local_docker.sh
```

## 11. VM 이미지 (OVA) 빌드 및 폐쇄망 배포

이 저장소의 모든 Ansible + OpenStack 실습 환경을 **VirtualBox OVA 이미지**로 패키징할 수 있습니다.

### 11.1 사전 요구 사항
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads) >= 6.1
- [Packer](https://developer.hashicorp.com/packer/install) >= 1.10

### 11.2 OVA 빌드
```bash
# Packer 플러그인 초기화 (최초 1회)
packer init packer/

# OVA 빌드 (약 30~60분 소요)
./scripts/build_ova.sh
```

빌드 결과물:
```
packer/output-ansible-openstack-lab/ansible-openstack-lab.ova
```

### 11.3 VirtualBox에 임포트 및 실행
```bash
VBoxManage import packer/output-ansible-openstack-lab/ansible-openstack-lab.ova \
    --vsys 0 --vmname "ansible-openstack-lab"
VBoxManage startvm "ansible-openstack-lab" --type headless

# SSH 접속 (호스트 포트 2222 → VM 포트 22)
ssh -p 2222 ansible@127.0.0.1   # 비밀번호: ansible
```

자세한 테스트 절차: [`docs/vm_image/virtualbox-test.md`](docs/vm_image/virtualbox-test.md)

### 11.4 폐쇄망(Air-Gapped) 환경 배포
OVA 이미지에는 pip 패키지 wheel, Ansible Galaxy 컬렉션이 미리 번들되어 있습니다.
폐쇄망 환경에서의 APT 미러, DNS, NTP, Docker 레지스트리, OpenStack 엔드포인트 설정 방법:

→ [`docs/vm_image/airgap-config.md`](docs/vm_image/airgap-config.md)

추가로, 같은 문서의 **3.8~3.9 절**에서 `Docker + Ollama + OpenStack` 사내망 서비스 구성 사례와
사내 GPU 장비 기준 Python LLM 호출 예시를 확인할 수 있습니다.
