# lecture09 - Docker Engine 설치 자동화

## 1. 강의 개요
- 강의 번호: `09`
- 모듈: `Module B / Ansible Operations`
- 난이도: `intermediate`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- Docker 엔진 설치/버전 점검 태스크 흐름을 이해한다.
- 운영 서버 표준 패키지 설치 절차를 정형화한다.
- 컨테이너 런타임 설치 후 기본 진단 명령을 익힌다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. reference docker engine playbook을 실행한다.
2. 강의 playbook으로 공통 진단 태스크를 수행한다.
3. install_enabled=true에서 docker 설치 여부를 확인한다.
4. docker version 결과를 로그에 기록한다.
5. 재실행 후 상태 변화를 점검한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행 (설치 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lecture09/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture09/playbook.yml -e install_enabled=true

# 레퍼런스 플레이북 실행
ansible-playbook -i ansible/inventories/local/hosts.ini ansible/playbooks/10_docker_engine_install.yml
```

## 6. 결과 확인 기준
- `PLAY RECAP` 기준 `failed=0`
- `Show lecture context` 출력 정상
- `Check Python3 availability` 출력 정상
- 재실행 시 변경량(`changed`) 추이 확인

## 7. 트러블슈팅 힌트
- 패키지 설치 실패: OS 패키지명/저장소 상태 확인
- 권한 오류: `become` 실행 권한 및 sudo 정책 확인
- 연결 오류: 인벤토리 호스트/connection 설정 확인

## 8. 참고 파일
- `./lecture.yml`
- `./playbook.yml`

## 유튜브 영상 찾아보기
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=lecture09+openstack+ansible)

