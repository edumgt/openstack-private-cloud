# lecture18 - Horizon 운영 점검과 로그 수집

## 1. 강의 개요
- 강의 번호: `18`
- 모듈: `Module E / OpenStack Operations`
- 난이도: `intermediate`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- Horizon 화면과 백엔드 상태를 연결해 점검한다.
- 운영 로그 수집 기준과 장애 1차 진단 절차를 만든다.
- API 기반 상태 확인 루틴을 정리한다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. 운영 점검 체크리스트를 준비한다.
2. 강의 playbook 실행으로 공통 루틴을 수행한다.
3. install_enabled=true 실행 결과를 기록한다.
4. 로그 분석 템플릿을 작성한다.
5. 장애 1차 대응 시퀀스를 정리한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행 (설치 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lecture18/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture18/playbook.yml -e install_enabled=true

# 레퍼런스 플레이북 실행
ansible-playbook -i ansible/inventories/local/hosts.ini ansible/playbooks/aws_outputs.yml
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
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=lecture18+openstack+ansible)

