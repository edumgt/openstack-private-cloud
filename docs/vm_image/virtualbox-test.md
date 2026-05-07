# VirtualBox VM 실행 테스트 가이드

이 문서는 `ansible-openstack-lab.ova`를 VirtualBox에 임포트하고
VM을 실행하여 기본 동작을 검증하는 절차를 설명합니다.

---

## 1. 사전 요구 사항

| 항목 | 버전 | 다운로드 |
|---|---|---|
| VirtualBox | >= 6.1 | https://www.virtualbox.org/wiki/Downloads |
| Packer | >= 1.10 | https://developer.hashicorp.com/packer/install |
| 호스트 RAM | >= 8 GB (VM에 4 GB 할당) | |
| 디스크 여유 공간 | >= 20 GB | |

---

## 2. OVA 빌드

> VirtualBox와 Packer가 설치된 인터넷 연결 환경에서 1회 실행

```bash
# 저장소 루트에서
./scripts/build_ova.sh
```

빌드가 완료되면 다음 위치에 OVA 파일이 생성됩니다.
```
packer/output-ansible-openstack-lab/ansible-openstack-lab.ova
```

---

## 3. VirtualBox에 OVA 임포트

### 3.1 GUI 방법

1. VirtualBox 메뉴 → **파일(File)** → **어플라이언스 가져오기(Import Appliance)**
2. OVA 파일 선택 후 **다음(Next)**
3. 가상 머신 이름, RAM(4 GB), CPU(2) 확인 후 **가져오기(Import)**

### 3.2 CLI 방법 (VBoxManage)

```bash
OVA_PATH="packer/output-ansible-openstack-lab/ansible-openstack-lab.ova"

# 임포트
VBoxManage import "${OVA_PATH}" \
    --vsys 0 \
    --vmname  "ansible-openstack-lab" \
    --memory  4096 \
    --cpus    2

# 네트워크: NAT (기본) + Host-Only 어댑터 추가
VBoxManage modifyvm "ansible-openstack-lab" \
    --nic1 nat \
    --nic2 hostonly \
    --hostonlyadapter2 vboxnet0

# VM 시작
VBoxManage startvm "ansible-openstack-lab" --type headless
```

---

## 4. SSH 접속

NAT 포트 포워딩이 자동 설정되어 있습니다 (호스트 2222 → VM 22).

```bash
ssh -p 2222 ansible@127.0.0.1
# 비밀번호: ansible
```

> 기본 계정: `ansible` / `ansible`  
> sudo 권한: 비밀번호 없이 사용 가능

---

## 5. 기본 동작 검증 (VM 내부)

SSH 접속 후 아래 항목을 순서대로 실행하세요.

### 5.1 환경 확인

```bash
# Python, Ansible 버전 확인
python3 --version
ansible --version

# 작업 디렉토리 이동
cd /opt/ansible-openstack
ls -la
```

### 5.2 Ansible 로컬 ping 테스트

```bash
ansible all \
    -i ansible/inventories/local/hosts.ini \
    -m ping
```

예상 출력:
```
localhost | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

### 5.3 lecture01 playbook 실행

```bash
ansible-playbook \
    -i ansible/inventories/local/hosts.ini \
    lecture01/playbook.yml \
    -e install_enabled=false
```

### 5.4 오프라인 pip 설치 테스트

```bash
WHEEL_DIR=/opt/ansible-openstack/offline/pip-wheels

pip install --no-index \
    --find-links="${WHEEL_DIR}" \
    ansible-core \
    && echo "[OK] 오프라인 pip 설치 성공"
```

### 5.5 Ansible Galaxy 컬렉션 목록 확인

```bash
ansible-galaxy collection list
```

---

## 6. 자동 검증 스크립트

VM 내부에서 한 번에 실행:

```bash
bash /opt/ansible-openstack/scripts/check.sh
```

---

## 7. VM 종료 및 스냅샷

```bash
# 스냅샷 생성 (호스트에서)
VBoxManage snapshot "ansible-openstack-lab" take "clean-install" \
    --description "초기 클린 상태"

# VM 전원 끄기
VBoxManage controlvm "ansible-openstack-lab" poweroff

# VM 삭제
VBoxManage unregistervm "ansible-openstack-lab" --delete
```

---

## 8. 네트워크 구성 옵션

| 모드 | 용도 | 설정 방법 |
|---|---|---|
| NAT | 호스트→인터넷 접근 | 기본값 (어댑터 1) |
| Host-Only | 호스트↔VM 직접 통신 | 어댑터 2, vboxnet0 |
| Bridged | VM이 실제 네트워크에 참여 | 어댑터 1을 Bridged로 변경 |
| Internal | VM 간 격리 네트워크 (폐쇄망 시뮬레이션) | 어댑터를 Internal Network로 변경 |

### 폐쇄망 시뮬레이션

```bash
# 어댑터를 Internal Network으로 변경 (인터넷 차단)
VBoxManage modifyvm "ansible-openstack-lab" \
    --nic1 intnet \
    --intnet1 "isolated-lab"
```

이후 [폐쇄망 구성 가이드](./airgap-config.md)를 참고해 설정하세요.

---

## 9. 문제 해결

| 증상 | 원인 | 해결 방법 |
|---|---|---|
| SSH 접속 실패 | VM이 아직 부팅 중 | 1분 대기 후 재시도 |
| `ansible` 명령어 없음 | PATH 미설정 | `source ~/.bashrc` 또는 `export PATH=$PATH:~/.local/bin` |
| pip install 실패 (폐쇄망) | 외부 PyPI 접근 불가 | `--no-index --find-links` 옵션 사용 |
| Galaxy 컬렉션 not found | COLLECTIONS_PATHS 미설정 | `export ANSIBLE_COLLECTIONS_PATHS=/opt/ansible-openstack/offline/collections` |
| VM 화면이 검은색 | headless 모드 | `VBoxManage startvm ... --type gui` 로 변경 |

## 유튜브 영상 찾아보기
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=virtualbox+test)

