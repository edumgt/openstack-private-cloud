# lecture02 - Inventory/Variables 구조 설계

## 1. 강의 개요
- 강의 번호: `02`
- 모듈: `Module A / Ansible Foundation`
- 난이도: `beginner`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- inventory 파일 구조와 그룹/호스트 변수 우선순위를 이해한다.
- 환경(dev/stage/prod) 분리를 위한 변수 설계 기준을 익힌다.
- 강의별 실행 인벤토리 선택 기준을 정리한다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. ansible/inventories/local/hosts.ini 구성 요소를 확인한다.
2. 강의 플레이북으로 변수 출력 흐름을 검증한다.
3. reference_playbook과 강의 playbook 차이를 비교한다.
4. install_enabled=true 실행 시 설치 태스크 동작을 확인한다.
5. 결과를 변수 설계 체크리스트로 정리한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행 (설치 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lecture02/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture02/playbook.yml -e install_enabled=true

# FastAPI 백엔드 컨테이너 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture02/playbook.yml -e deploy_backend=true

# 레퍼런스 플레이북 실행
ansible-playbook -i ansible/inventories/local/hosts.ini ansible/playbooks/00_bootstrap.yml
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


---
```
ansible-playbook -i ansible/inventories/local/hosts.ini lecture02/playbook.yml -e deploy_backend=true
```

### playbook 수정

---
```
ansible-playbook lecture02/md.yaml
```

## 유튜브 영상 찾아보기
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=lecture02+openstack+ansible)

