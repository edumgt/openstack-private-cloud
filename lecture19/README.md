# lecture19 - 실제 OpenStack 클라이언트 환경 준비

## 1. 강의 개요
- 강의 번호: `19`
- 모듈: `Module E / OpenStack Operations`
- 난이도: `intermediate`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- 실제 OpenStack API에 연결할 클라이언트 환경을 준비한다.
- `openrc`와 `clouds.yaml`을 생성한다.
- 별도 Ubuntu 서버에 `DevStack`을 올릴 수 있도록 사전 준비를 수행한다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 실제 OpenStack API 또는 DevStack 설치 대상 Ubuntu 서버 준비
- 인벤토리 파일 확인: `ansible/inventories/dev/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. OpenStack 인증 환경 변수 또는 실제 API 주소를 준비한다.
2. `lecture19/playbook.yml`로 `real-openstack-openrc`와 `clouds.yaml`을 만든다.
3. 별도 서버가 있으면 `ansible/playbooks/30_devstack_host_prep.yml`로 DevStack 설치 준비를 한다.
4. `stack.sh` 실행 후 Keystone URL을 확인한다.
5. `lecture20`, `lecture21`로 검증을 이어간다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 실제 OpenStack 클라이언트 환경 준비
export OS_AUTH_URL=http://<REAL_OPENSTACK_IP>:5000/v3
export OS_USERNAME=admin
export OS_PASSWORD=<PASSWORD>
export OS_PROJECT_NAME=admin

ansible-playbook -i ansible/inventories/local/hosts.ini lecture19/playbook.yml -e install_enabled=true

# 별도 Ubuntu 서버에 DevStack 설치 준비
ansible-playbook -i ansible/inventories/dev/hosts.ini ansible/playbooks/30_devstack_host_prep.yml -l openstack_hosts

# 대상 서버에서 DevStack 실제 설치
sudo -iu stack bash -lc 'cd /opt/devstack/devstack && ./stack.sh'
```

## 6. 결과 확인 기준
- `PLAY RECAP` 기준 `failed=0`
- `.lab/real-openstack-openrc` 생성 확인
- `/root/.config/openstack/clouds.yaml` 생성 확인
- DevStack 서버에 `/opt/devstack/devstack/local.conf` 생성 확인
- DevStack 설치 후 `http://<server-ip>:5000/v3` 응답 확인

## 7. 트러블슈팅 힌트
- WSL2 로컬 머신은 실제 OpenStack 제어면 호스트로 비권장
- DevStack은 별도 Ubuntu 서버(권장 8 vCPU / 16GB RAM 이상)에서 실행
- `5000/tcp` timeout: 방화벽, 라우팅, DevStack `stack.sh` 로그 확인
- `openstack token issue` 실패: `real-openstack-openrc` 값과 Keystone 상태 확인

## 8. 참고 파일
- `./lecture.yml`
- `./playbook.yml`
- `../ansible/playbooks/30_devstack_host_prep.yml`

## 유튜브 영상 찾아보기
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=lecture19+openstack+ansible)

