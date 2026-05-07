# lecture03 - Ad-hoc 명령과 Facts 수집 자동화

## 1. 강의 개요
- 강의 번호: `03`
- 모듈: `Module A / Ansible Foundation`
- 난이도: `beginner`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- Ad-hoc 명령과 playbook 실행의 차이를 이해한다.
- facts 수집 결과를 진단/분기 로직에 활용하는 방법을 익힌다.
- 실패 시 원인-증상-조치 순서의 점검 루틴을 만든다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. ad-hoc ping과 command 예시를 실행한다.
2. 강의 playbook으로 facts 수집 상태를 확인한다.
3. reference playbook 실행 결과와 비교한다.
4. 설치 포함 실행에서 태스크 변화(changed/ok)를 확인한다.
5. 트러블슈팅 포인트를 문서화한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행 (설치 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lecture03/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture03/playbook.yml -e install_enabled=true

# 레퍼런스 플레이북 실행
ansible-playbook -i ansible/inventories/local/hosts.ini ansible/playbooks/learning/01_ping.yml
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
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=lecture03+openstack+ansible)

