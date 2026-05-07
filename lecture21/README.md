# lecture21 - OpenStack/Nova 기본 점검

## 1. 강의 개요
- 강의 번호: `21`
- 모듈: `Module E / OpenStack Operations`
- 난이도: `intermediate`
- 권장 시간: `30분`

## 2. 상세 학습 내용
- `openstack` CLI로 Keystone 인증이 되는지 확인한다.
- `nova service list`와 `hypervisor list`를 조회한다.
- `compute1`, `compute2`를 동적 인벤토리로 등록한다.
- 두 서버에 `nginx`를 설치하고 80 포트 HTTP 응답을 확인한다.
- Codespaces mock 환경과 실제 OpenStack 환경을 같은 플레이북으로 점검한다.

## 3. 실행 전 체크
- `lecture22`를 먼저 실행해 mock 환경 또는 인증 정보를 준비
- `.venv/bin/openstack` 설치 여부 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- mock 환경 기본 인증 엔드포인트는 `http://127.0.0.1:15000/v3`
- 실제 OpenStack에서는 `compute1`, `compute2`에 SSH 가능해야 함
- 보안 그룹 또는 방화벽에서 `22/tcp`, `80/tcp` 허용 필요
- 기본값은 floating IP 우선이며, floating IP가 없으면 SSH 배포를 중단함
- 필요 시 `OPENSTACK_SSH_KEY_PATH` 또는 `-e compute_ssh_private_key_file=...` 지정
- `lecture22` mock openrc를 사용하면 OpenStack 조회까지만 수행하고, 원격 `nginx` 배포는 자동으로 건너뜀

## 4. 실습 절차
1. Keystone 엔드포인트 응답을 확인한다.
2. `openstack token issue` 결과를 확인한다.
3. `openstack compute service list` 결과를 기록한다.
4. `openstack hypervisor list` 결과를 기록한다.
5. `compute1`, `compute2`의 접속 IP를 식별한다.
6. 두 서버에 `nginx`를 설치하고 서비스 기동을 확인한다.
7. 각 서버의 `http://<ip>:80` 접속 결과를 확인한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# lecture22 이후 실행
source .lab/keystone-admin-openrc
ansible-playbook -i ansible/inventories/local/hosts.ini lecture21/playbook.yml -e install_enabled=false

# lecture21에서 필요한 패키지까지 같이 준비
ansible-playbook -i ansible/inventories/local/hosts.ini lecture21/playbook.yml -e install_enabled=true

# SSH 사용자/키를 함께 지정하는 예시
ansible-playbook -i ansible/inventories/local/hosts.ini lecture21/playbook.yml \
  -e install_enabled=false \
  -e compute_ssh_user=ubuntu \
  -e compute_ssh_private_key_file=~/.ssh/openstack.pem

# floating IP 대신 직접 접속 가능한 IP를 강제로 지정하는 예시
ansible-playbook -i ansible/inventories/local/hosts.ini lecture21/playbook.yml \
  -e install_enabled=false \
  -e 'compute_access_ip_overrides={"compute1":"192.168.0.101","compute2":"192.168.0.102"}'
```

### 5.1 실제 OpenStack openrc 파일이 없을 때
```bash
export OS_AUTH_URL=http://<OPENSTACK_IP>:5000/v3
export OS_USERNAME=admin
export OS_PASSWORD=<PASSWORD>
export OS_PROJECT_NAME=admin
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_DOMAIN_NAME=Default
export OS_REGION_NAME=RegionOne
export OS_INTERFACE=public
export OS_IDENTITY_API_VERSION=3

bash scripts/create_real_openrc.sh "$PWD"
source .lab/real-openstack-openrc
```

그 다음 실제 OpenStack에서 `floating IP`를 붙이고 배포합니다.

```bash
openstack floating ip create public
openstack server add floating ip compute1 <FLOATING_IP_1>
openstack floating ip create public
openstack server add floating ip compute2 <FLOATING_IP_2>

/home/Ansible-Openstack-Private-Cloud/.venv/bin/ansible-playbook \
  -i ansible/inventories/local/hosts.ini \
  lecture21/playbook.yml \
  -e openrc_path="$PWD/.lab/real-openstack-openrc" \
  -e compute_ssh_user=ubuntu \
  -e compute_ssh_private_key_file=~/.ssh/openstack.pem
```

## 6. 결과 확인 기준
- `PLAY RECAP` 기준 `failed=0`
- `token_rc=0`
- `nova_service_rc=0`
- `hypervisor_rc=0`
- 서비스/하이퍼바이저 목록이 출력됨
- `compute1`, `compute2`에 `nginx`가 설치되고 서비스가 실행됨
- 제어 노드에서 `http://<compute-access-ip>:80` 확인 시 `200` 응답
- 단, 위 배포 결과 검증은 실제 OpenStack 인증 정보 사용 시에만 해당

## 7. 트러블슈팅 힌트
- `openstack` 명령 없음: `lecture22`를 `install_enabled=true`로 다시 실행
- `keystone_http_status`가 `200`이 아님: mock 서버 또는 실제 Keystone 상태 확인
- Nova 조회 실패: 인증 정보 또는 compute endpoint 확인
- SSH 연결 실패: `compute_ssh_user`, 개인키 경로, security group의 `22/tcp` 허용 확인
- `10.x.x.x` 같은 fixed IP timeout: tenant 내부망만 붙어 있는 상태일 수 있으니 floating IP 연결 또는 `compute_access_ip_overrides` 사용
- HTTP 80 실패: 인스턴스 security group의 `80/tcp` 허용 여부와 `nginx` 서비스 상태 확인
- mock 환경은 floating IP/SSH 대상이 없으므로 실제 SSH/nginx 배포 검증은 실제 OpenStack 인스턴스에서 수행

## 8. 참고 파일
- `./lecture.yml`
- `./playbook.yml`
- `../lecture22/playbook.yml`

## 유튜브 영상 찾아보기
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=lecture21+openstack+ansible)

