# OpenStack Infra Design (Nova + Swift + Octavia 통합 설계)

---

## 1. 개요

본 문서는 OpenStack 환경에서 다음 요소를 통합한 인프라 설계를 정리한다.

* Nova (Compute)
* Neutron (Network)
* Cinder (Block Storage)
* Swift (Object Storage)
* Octavia (Load Balancer)

---

## 2. 현재 YAML 기반 구성 분석

현재 Ansible Playbook은 다음 항목을 점검한다.

### 주요 검증 항목

* Keystone 인증 확인
* Nova Compute 서비스 상태
* Hypervisor 상태
* Neutron Network 조회
* Cinder Volume 조회
* compute1 / compute2 존재 여부

### 구조 특징

* compute1, compute2 존재
* net-compute1, net-compute2 (분리 네트워크)
* vol-compute1, vol-compute2 (분리 볼륨)

### 결론

현재 구조는:

```
compute1 → net-compute1 → vol-compute1
compute2 → net-compute2 → vol-compute2
```

즉,

> "각 compute가 완전히 독립된 네트워크 + 스토리지 구조"

✔ 공유 스토리지 구조 아님

---

## 3. Swift (Object Storage)

### 개념

Swift는 OpenStack의 오브젝트 스토리지이다.

* S3 유사 구조
* API 기반 접근
* Container / Object 구조

### 특징

| 항목    | 설명       |
| ----- | -------- |
| 접근 방식 | REST API |
| 저장 방식 | Object   |
| 공유 방식 | API      |

### 사용 용도

* 파일 업로드 저장소
* 이미지 저장
* 백업
* 로그 저장

### 제한사항

Swift는 아래 용도로는 부적합

* 공유 디스크 (/mnt/shared)
* DB 파일 시스템
* POSIX 파일 접근

---

## 4. Octavia (Load Balancer)

### 개념

OpenStack의 LBaaS 서비스

### 기능

* L4 / L7 Load Balancing
* VIP 제공
* Health Check
* Failover

### 구성 요소

* LoadBalancer
* Listener
* Pool
* Member
* Health Monitor

---

## 5. 통합 아키텍처

```
               [ User ]
                  │
             (DNS Name)
                  │
          [ Octavia VIP ]
            /         \
     compute1       compute2
        (VM)           (VM)
            \         /
             \       /
               [ Swift ]
```

---

## 6. 동작 흐름

1. 사용자가 DNS로 접근
2. DNS → Octavia VIP
3. Octavia → compute1 / compute2 분산
4. 서버 → Swift에 파일 저장

---

## 7. "공유 스토리지" 개념 비교

### Swift

* API 기반 공유
* 파일 업로드/다운로드
* 디스크처럼 사용 불가

---

### 공유 파일 시스템 필요 시

다음 서비스 필요

* NFS
* CephFS
* Manila

---

## 8. 설계 패턴

### 패턴 A (추천)

```
Octavia + Swift
```

* 서비스 이중화
* 파일 저장 분리
* 가장 일반적인 구조

---

### 패턴 B (파일 공유 필요)

```
Octavia + Swift + NFS/Manila
```

---

### 패턴 C (고급)

```
Ceph + Nova + Cinder
```

* 라이브 마이그레이션
* 고가용성

---

## 9. YAML 기준 한계

현재 YAML은 다음만 검증

* Nova
* Neutron
* Cinder

즉,

> Swift / Octavia 관련 검증 없음

---

## 10. Swift 검증 추가

### CLI

```
openstack container list
openstack object store account show
```

### 검증 항목

* Container 존재 여부
* Object 업로드 테스트

---

## 11. Octavia 검증 추가

```
openstack loadbalancer list
openstack loadbalancer listener list
openstack loadbalancer pool list
openstack loadbalancer member list
```

### 검증 항목

* VIP 생성 여부
* Backend 연결 상태
* Health Check 정상 여부

---

## 12. DNS 구조

```
app.company.local → Octavia VIP
```

✔ compute 직접 접근 금지
✔ 항상 VIP 통해 접근

---

## 13. 핵심 비교 정리

| 항목        | Swift  | 공유 파일 시스템 |
| --------- | ------ | --------- |
| 접근        | API    | Mount     |
| 구조        | Object | File      |
| 용도        | 저장     | 공유        |
| 실시간 동시 접근 | 제한적    | 가능        |

---

## 14. 최종 결론

| 기능          | 가능 여부       |
| ----------- | ----------- |
| DNS 기반 접속   | 가능          |
| Swift 기반 공유 | 가능 (API 방식) |
| 디스크 공유      | 불가          |
| Octavia 이중화 | 가능          |

---

## 15. 최종 추천 구조

```
Octavia + Swift + (필요 시 NFS/Manila)
```

---

## 16. 핵심 요약

* Swift = 공용 저장소 (Object)
* Octavia = 트래픽 진입점
* Compute 2대 = 서비스 처리
* 공유 디스크 필요 시 → Manila/NFS 추가

---

## 17. 확장 방향

* Ceph 도입 → 고급 스토리지
* Designate → DNS 자동화
* Auto Scaling → Compute 확장
* CI/CD → 서비스 자동 배포

---

# END

## 유튜브 영상 찾아보기
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=openstack+swift+octavia+design)

