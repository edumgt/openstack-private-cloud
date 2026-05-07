# lecture22 - Codespaces용 Keystone/Nova Mock 준비

## 1. 강의 개요
- 강의 번호: `22`
- 모듈: `Module E / OpenStack Operations`
- 난이도: `intermediate`
- 권장 시간: `30분`

## 2. 상세 학습 내용
- Codespaces에서 `ansible-core`와 `python-openstackclient`를 준비한다.
- 로컬 mock Keystone/Nova API를 실행한다.
- `lecture21`에서 재사용할 `openrc` 파일을 생성한다.
- 기존 Apache/Keystone와 충돌하지 않도록 mock API는 `15000~15004` 중 사용 가능한 포트를 자동 선택한다.
- 브라우저에서 상태를 볼 수 있도록 Horizon-style dashboard를 함께 제공한다.

## 3. 실행 전 체크
- Codespaces 또는 devcontainer 환경 진입
- 프로젝트 루트에서 `.venv` 활성화 여부 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`

## 4. 실습 절차
1. `install_enabled=true`로 Python 패키지를 준비한다.
2. mock Keystone/Nova 서버를 실행한다.
3. `.lab/keystone-admin-openrc` 파일을 생성한다.
4. `openstack token issue`가 성공하는지 확인한다.
5. `lecture21`을 실행해 Nova 서비스/하이퍼바이저 조회까지 확인한다.
6. `/dashboard` 페이지에서 웹 상태 화면을 확인한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 1) Codespaces 기본 준비
bash .devcontainer/post-create.sh

# 2) lecture22 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture22/playbook.yml -e install_enabled=true

# 3) 인증 정보 적용
source .lab/keystone-admin-openrc

# 4) dashboard 확인
echo "$OS_AUTH_URL"   # 예: http://127.0.0.1:15000/v3
# 브라우저에서 http://127.0.0.1:15000/dashboard 접속

# 5) lecture21 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture21/playbook.yml -e install_enabled=false
```

## 6. 결과 확인 기준
- `PLAY RECAP` 기준 `failed=0`
- `.venv/bin/openstack --version` 출력 정상
- 선택된 포트의 `/healthz` 응답 정상
- `.lab/keystone-admin-openrc` 파일 생성 확인
- 선택된 포트의 `/dashboard` 페이지 접속 정상

## 7. 트러블슈팅 힌트
- `openstack` 명령 없음: `bash .devcontainer/post-create.sh` 또는 `install_enabled=true` 재실행
- mock 포트 충돌: `.lab/openstack-mock/server.pid` 확인 후 `scripts/stop_mock_openstack.sh` 실행
- mock 서버 비정상: `.lab/openstack-mock/server.log` 확인

## 8. 참고 파일
- `./lecture.yml`
- `./playbook.yml`
- `../scripts/mock_openstack_api.py`

## 유튜브 영상 찾아보기
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=lecture22+openstack+ansible)

