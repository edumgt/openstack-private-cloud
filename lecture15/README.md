# lecture15 - Glance 이미지 관리 자동화

## 1. 강의 개요
- 강의 번호: `15`
- 모듈: `Module D / OpenStack Foundation`
- 난이도: `intermediate`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- 이미지 등록/조회/상태 관리 라이프사이클을 이해한다.
- 메타데이터와 이미지 스토어 분리 개념을 학습한다.
- 이미지 버전 관리 규칙을 정의한다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. Glance 라이프사이클 단계(등록/검증/배포)를 정리한다.
2. 강의 playbook 실행으로 기본 루틴을 검증한다.
3. install_enabled=true 결과를 확인한다.
4. 이미지 네이밍 규칙을 설계한다.
5. 운영 체크리스트를 작성한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행 (설치 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lecture15/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture15/playbook.yml -e install_enabled=true

# 레퍼런스 플레이북 실행
ansible-playbook -i ansible/inventories/local/hosts.ini ansible/playbooks/11_deploy_stack.yml
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
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=lecture15+openstack+ansible)

