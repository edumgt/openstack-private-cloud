# lecture24 - Octavia Load Balancer 점검

## 1. 강의 개요
- 강의 번호: `24`
- 모듈: `Module E / OpenStack Operations`
- 난이도: `intermediate`
- 권장 시간: `50분`

## 2. 상세 학습 내용
- Octavia Load Balancer as a Service (LBaaS) 개념을 이해한다.
- 두 compute 또는 그 위 VM 서비스들을 하나의 진입점으로 묶는 방법을 학습한다.
- Load Balancer, Listener, Pool, Member 구조를 이해한다.
- Health Monitor로 자동 장애 조치를 구성한다.
- 실제 트래픽 분산 시나리오를 테스트한다.

## 3. Octavia 사용 사례
- **웹 서비스 HA**: 여러 웹 서버를 하나의 VIP로 묶기
- **API Gateway**: 마이크로서비스 앞단 부하 분산
- **Compute 이중화**: compute1, compute2를 단일 진입점으로 통합
- **자동 장애 조치**: Health check로 장애 서버 자동 제외

## 4. 실행 전 체크
- Python/Ansible 버전 확인
- OpenStack 인증 정보 (실제 환경 또는 Mock)
- Octavia 서비스 설치 여부 확인
- Neutron 네트워크 존재 확인
- 최소 2대의 compute 인스턴스 또는 테스트 VM 필요
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`

## 5. 실습 절차
1. Octavia 서비스 endpoint 확인
2. Load Balancer 생성 (`openstack loadbalancer create`)
3. Listener 추가 (포트 80 HTTP)
4. Pool 생성 (Round Robin 알고리즘)
5. Member 추가 (compute1, compute2의 private IP)
6. Health Monitor 설정
7. VIP(Virtual IP)로 트래픽 테스트
8. 한 서버 중지 후 자동 장애 조치 확인

## 6. 실행 방법 (프로젝트 루트에서 실행)

### 6.1 실제 OpenStack 환경
```bash
# Octavia 서비스 확인
source .lab/real-openstack-openrc
.venv/bin/openstack service list | grep load-balancer

# lecture24 실행 (Octavia가 설치된 경우)
.venv/bin/ansible-playbook -i ansible/inventories/local/hosts.ini \
  lecture24/playbook.yml \
  -e install_enabled=false \
  -e openrc_path=.lab/real-openstack-openrc \
  -e use_mock_openstack_auth=false \
  -e lb_vip_subnet=private-subnet
```

### 6.2 Mock 환경 (Octavia 미설치 시)
```bash
# Mock 환경에서 개념 학습
.venv/bin/ansible-playbook -i ansible/inventories/local/hosts.ini \
  lecture24/playbook.yml \
  -e install_enabled=false \
  -e octavia_service_available=false
```

## 7. Load Balancer 구성 요소
```
Load Balancer
  └─ Listener (포트 80)
       └─ Pool (Round Robin)
            ├─ Member: compute1 (10.0.0.11:80)
            ├─ Member: compute2 (10.0.0.12:80)
            └─ Health Monitor (HTTP GET /)
```

## 8. 결과 확인 기준
- `PLAY RECAP` 기준 `failed=0`
- Octavia 서비스 설치 시:
  - Load Balancer 생성 성공
  - VIP 할당 성공
  - 트래픽 분산 확인 (compute1, compute2 번갈아 응답)
  - Health check 동작 확인
- Octavia 미설치 시:
  - 서비스 부재 확인
  - 대체 방안 안내 (HAProxy, Nginx 등)

## 9. 트러블슈팅 힌트
- Octavia 서비스 없음: `service list`에서 `load-balancer` 확인
- Amphora 이미지 없음: amphora-x64-haproxy 이미지 확인
- Member 추가 실패: 서브넷 및 보안 그룹 확인
- VIP 접근 불가: floating IP 연결 확인

## 10. 참고 파일
- `./lecture.yml`
- `./playbook.yml`

## 11. 추가 학습 자료
- OpenStack Octavia 공식 문서: https://docs.openstack.org/octavia/latest/
- Amphora 구조 이해
- Load Balancing 알고리즘 (Round Robin, Least Connections, Source IP)

## 유튜브 영상 찾아보기
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=lecture24+openstack+ansible)

