# 📄 OpenStack Nova 테스트 환경 구축 (Ansible 기반)

## 1. 개요

OpenStack 환경에서 Nova(Compute)를 테스트하려면  
단독 서비스 설치가 아닌 **전체 OpenStack 최소 구성**이 필요하다.

대표적인 구축 방식:

- DevStack → 빠른 테스트
- Kolla-Ansible → 실무형 테스트 (추천)
- OpenStack-Ansible → 운영 환경

---

## 2. 구성 방식 선택

| 목적 | 방식 |
|------|------|
| 빠른 테스트 | DevStack |
| Ansible 기반 실무 테스트 | Kolla-Ansible |
| 운영 환경 구축 | OpenStack-Ansible |

---

## 3. 추천: Kolla-Ansible 방식

### 특징

- Docker 기반 OpenStack
- 빠른 설치 및 복구
- Ansible 자동화 가능
- 멀티노드 확장 가능

---

## 4. 아키텍처

```
[ Control Node ]
 - Keystone
 - Nova API
 - Glance
 - Neutron

[ Compute Node ]
 - Nova Compute (VM 실행)

[ Network Node ]
 - Neutron L3 / DHCP

[ Storage Node ]
 - Cinder / Ceph
```

👉 테스트용은 **All-in-One (1노드)** 가능

---

## 5. 사전 준비

### OS

- Ubuntu 20.04 / 22.04 / 24.04 추천

### 패키지 설치

```bash
sudo apt update
sudo apt install -y python3-dev libffi-dev gcc libssl-dev python3-pip
```

---

## 6. Kolla-Ansible 설치

```bash
pip install 'ansible>=6,<8'
pip install kolla-ansible
```

---

## 7. 초기 설정

### 의존성 설치

```bash
kolla-ansible install-deps
```

### 패스워드 생성

```bash
kolla-genpwd
```

### 설정 복사

```bash
cp -r /usr/local/share/kolla-ansible/etc_examples/kolla/* /etc/kolla
```

---

## 8. Inventory 설정

```bash
cp /usr/local/share/kolla-ansible/ansible/inventory/all-in-one .
```

👉 단일 노드 테스트 가능

---

## 9. globals.yml 설정

```yaml
kolla_base_distro: "ubuntu"
kolla_install_type: "source"

network_interface: "eth0"

enable_nova: "yes"
enable_neutron: "yes"
enable_glance: "yes"
enable_keystone: "yes"
```

---

## 10. 배포 실행

```bash
kolla-ansible -i all-in-one bootstrap-servers
kolla-ansible -i all-in-one prechecks
kolla-ansible -i all-in-one deploy
kolla-ansible post-deploy
```

---

## 11. 결과 확인

### OpenStack CLI 환경 설정

```bash
source /etc/kolla/admin-openrc.sh
```

### VM 생성 테스트

```bash
openstack server list
```

---

## 12. Horizon 접속

```
http://<서버IP>
```

계정:
```
admin / admin_password
```

---

## 13. DevStack (간단 테스트용)

```bash
git clone https://opendev.org/openstack/devstack
cd devstack

cat <<EOF > local.conf
[[local|localrc]]
ADMIN_PASSWORD=secret
DATABASE_PASSWORD=secret
RABBIT_PASSWORD=secret
SERVICE_PASSWORD=secret
EOF

./stack.sh
```

---

## 14. Nova 구성 요소 (핵심 이해)

| 구성 요소 | 역할 |
|----------|------|
| nova-api | API 서버 |
| nova-scheduler | VM 배치 결정 |
| nova-conductor | DB 중계 |
| nova-compute | VM 실행 |
| placement | 리소스 관리 |

---

## 15. 실무 핵심 포인트

- Nova 단독 실행 불가 → 반드시 아래 필요
  - Keystone
  - Neutron
  - Glance
  - Placement

- 테스트 순서 추천

```
1. DevStack → 개념 이해
2. Kolla-Ansible → 구조 이해
3. Multi-node → 확장 테스트
```

---

## 16. 확장 (다음 단계)

- Ceph 연동 (스토리지)
- Octavia (로드밸런서)
- Swift (Object Storage)
- Kubernetes 연동

---

## 17. 한 줄 정리

👉 Nova 테스트 = OpenStack 최소 클러스터 필요  
👉 가장 현실적인 방법 = **Kolla-Ansible**

---

## 18. 참고 링크

- Nova GitHub (Mirror): https://github.com/openstack/nova  
- 공식 저장소: https://opendev.org/openstack/nova

## 유튜브 영상 찾아보기
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=openstack+nova+ansible+guide)

