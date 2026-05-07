# Kubernetes vs OpenStack Node 비교 정리

## 1. 개요

Kubernetes와 OpenStack은 구조가 비슷해 보이지만 역할이 다르다.

- Kubernetes: 컨테이너 오케스트레이션 플랫폼
- OpenStack: 가상 인프라(IaaS) 플랫폼

---

## 2. 전체 구조 비교

| 구분 | Kubernetes | OpenStack |
|------|------------|-----------|
| 목적 | 컨테이너 관리 | VM/네트워크/스토리지 관리 |
| Control Plane | Control Node (Master) | Controller Node |
| 실행 노드 | Worker Node | Compute Node |
| 실행 대상 | Pod (컨테이너) | VM (Instance) |

---

## 3. Control Node vs Controller Node

### Kubernetes Control Node

클러스터의 두뇌 역할

#### 구성 요소
- API Server: 모든 요청의 진입점
- Scheduler: Pod 배치 결정
- Controller Manager: 상태 유지
- etcd: 클러스터 상태 저장

#### 역할
- 컨테이너 배치 결정
- 클러스터 상태 관리

---

### OpenStack Controller Node

클라우드 관리 서버

#### 구성 요소
- Keystone: 인증
- Nova API: VM 생성 요청 처리
- Glance: 이미지 관리
- Neutron: 네트워크 관리
- Cinder: 스토리지 관리
- Horizon: 웹 UI

#### 역할
- VM 생성 요청 처리
- 인증/네트워크/스토리지 관리

---

### 핵심 차이

| Kubernetes Control | OpenStack Controller |
|-------------------|---------------------|
| Pod 스케줄링 | VM 생성 요청 처리 |
| etcd 사용 | DB + 메시지 큐 |
| 컨테이너 중심 | 인프라 중심 |

---

## 4. Worker Node vs Compute Node

### Kubernetes Worker Node

컨테이너 실행 서버

#### 구성
- kubelet: Control Plane과 통신
- container runtime (containerd, docker)
- kube-proxy: 네트워크 처리

#### 역할
- Pod 실행
- 상태 보고
- 컨테이너 lifecycle 관리

---

### OpenStack Compute Node

VM 실행 서버

#### 구성
- Nova Compute
- Hypervisor (KVM/QEMU)
- Neutron Agent

#### 역할
- VM 생성/삭제
- CPU/RAM 리소스 할당
- 하이퍼바이저 기반 실행

---

### 핵심 차이

| Kubernetes Worker | OpenStack Compute |
|------------------|-------------------|
| Pod 실행 | VM 실행 |
| container runtime | Hypervisor |
| kubelet | nova-compute |
| 빠름/경량 | 무거움/격리 강함 |

---

## 5. 계층 구조

## 유튜브 영상 찾아보기
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=k8s+vs+openstack)

