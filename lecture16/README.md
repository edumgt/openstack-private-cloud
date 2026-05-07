# lecture16 - Nova 인스턴스 라이프사이클 자동화

## 1. 강의 개요
- 강의 번호: `16`
- 모듈: `Module D / OpenStack Foundation`
- 난이도: `intermediate`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- 인스턴스 생성/조회/삭제/상태 전이 흐름을 이해한다.
- 스케줄러/컴퓨트 역할 분리를 운영 관점으로 정리한다.
- 실패 시 진단 포인트(API/DB/MQ)를 학습한다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. Nova 요청 흐름(API→Scheduler→Compute)을 정리한다.
2. 강의 playbook 실행 결과를 기록한다.
3. install_enabled=true 결과를 확인한다.
4. 상태 전이 표를 작성한다.
5. 장애 대응 우선순위를 문서화한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행 (설치 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lecture16/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture16/playbook.yml -e install_enabled=true

# 레퍼런스 플레이북 실행
ansible-playbook -i ansible/inventories/local/hosts.ini ansible/playbooks/12_deploy_stack_rolling.yml
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
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=lecture16+openstack+ansible)

