# 00. 실습 환경 준비

## 1) Ansible 실행 환경
Ansible 컨트롤 노드(명령을 실행하는 PC)는 보통 Linux가 가장 편합니다.

### 권장
- Windows 11 + WSL2(Ubuntu) + Python + Ansible
- 또는 macOS

### 최소 요구
- Python 3.9+
- SSH 접속 가능한 리눅스 대상(또는 localhost)

## 2) 설치(WSL Ubuntu 예시)
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip ssh
pip3 install -U pip
pip3 install ansible
```

## 3) AWS 준비
- AWS CLI 설치 후 로그인/프로파일 구성 또는 Access Key 발급

### 자격증명 확인
```bash
aws sts get-caller-identity
```

## 4) Docker 대상 호스트 준비
- Docker를 설치할 대상이 로컬이면 `localhost`
- 원격이면 `ansible/inventories/docker/hosts.ini`에 IP/계정을 추가

## 유튜브 영상 찾아보기
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=openstack+ansible+prereqs)

