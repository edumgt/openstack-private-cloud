# lecture01 - Ansible 학습환경 점검과 실행 루틴 정립

## 1. 강의 개요
- 강의 번호: `01`
- 모듈: `Module A / Ansible Foundation`
- 난이도: `beginner`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- 컨트롤 노드/관리 노드 구조를 이해하고 로컬 실습 환경을 점검한다.
- Ansible 기본 실행 흐름(ping, playbook 실행, 결과 확인)을 익힌다.
- 실행 로그를 표준 포맷으로 남기는 루틴을 만든다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. 가상환경 또는 시스템 Ansible 버전을 확인한다.
2. lecture playbook을 install_enabled=false로 실행한다.
3. debug 출력과 Python 버전 확인 태스크를 검증한다.
4. install_enabled=true로 재실행해 패키지 설치 루틴을 확인한다.
5. 결과 로그를 저장하고 회고 메모를 기록한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행 (설치 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lecture01/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture01/playbook.yml -e install_enabled=true

# 레퍼런스 플레이북 실행
ansible-playbook -i ansible/inventories/local/hosts.ini ansible/playbooks/00_ping.yml
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
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=lecture01+openstack+ansible)

