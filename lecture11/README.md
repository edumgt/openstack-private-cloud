# lecture11 - AWS SSM 연결 기반 운영 브릿지

## 1. 강의 개요
- 강의 번호: `11`
- 모듈: `Module C / Cloud Bridge`
- 난이도: `intermediate`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- SSH 없이 SSM 기반 관리 흐름을 이해한다.
- 클라우드 운영 접근 제어 관점을 학습한다.
- OpenStack 인증/접근 모델과 비교 포인트를 정리한다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. SSM reference playbook 구성을 검토한다.
2. 강의 playbook 실행으로 기본 진단을 수행한다.
3. install_enabled=true 실행 시 패키지 설치 결과를 확인한다.
4. AWS 자격정보 필요 조건을 정리한다.
5. OpenStack Keystone 대응 개념을 메모한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행 (설치 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lecture11/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture11/playbook.yml -e install_enabled=true

# 레퍼런스 플레이북 실행
ansible-playbook -i ansible/inventories/local/hosts.ini ansible/playbooks/20_aws_provision_ssm_no_ssh.yml
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
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=lecture11+openstack+ansible)

