# lecture04 - Jinja2 템플릿과 Handler 실전

## 1. 강의 개요
- 강의 번호: `04`
- 모듈: `Module A / Ansible Foundation`
- 난이도: `beginner`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- Jinja2 템플릿 변수 바인딩 패턴을 익힌다.
- 변경이 있을 때만 handler가 동작하는 구조를 이해한다.
- 템플릿 파일과 역할(role) 구조의 연결 방식을 학습한다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. 템플릿/핸들러가 포함된 reference playbook을 확인한다.
2. 강의 playbook 실행 후 로그를 수집한다.
3. 재실행으로 idempotency를 확인한다.
4. 설치 포함 실행으로 환경 편차를 검증한다.
5. 변경 발생 조건과 handler 트리거 조건을 정리한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행 (설치 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lecture04/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture04/playbook.yml -e install_enabled=true

# 레퍼런스 플레이북 실행
ansible-playbook -i ansible/inventories/local/hosts.ini ansible/playbooks/learning/04_template_handler.yml
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
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=lecture04+openstack+ansible)

