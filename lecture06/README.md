# lecture06 - Idempotency와 검증 자동화

## 1. 강의 개요
- 강의 번호: `06`
- 모듈: `Module A / Ansible Foundation`
- 난이도: `beginner`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- 멱등성(idempotency) 관점에서 자동화 품질 기준을 이해한다.
- check/diff/재실행 결과를 비교하는 방법을 학습한다.
- 검증 태스크를 플레이북에 내장하는 패턴을 익힌다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. 동일 플레이북을 2회 이상 실행해 changed 추이를 본다.
2. 실패/성공 로그 비교 포인트를 정리한다.
3. reference 검증 플레이북 실행 결과를 확인한다.
4. 설치 포함 실행으로 환경 의존성 이슈를 점검한다.
5. 품질 체크리스트를 완성한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행 (설치 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lecture06/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture06/playbook.yml -e install_enabled=true

# 레퍼런스 플레이북 실행
ansible-playbook -i ansible/inventories/local/hosts.ini ansible/playbooks/check_nginx.yml
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
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=lecture06+openstack+ansible)

