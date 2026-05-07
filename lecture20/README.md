# lecture20 - 종합 캡스톤: OpenStack 운영 Runbook 완성

## 1. 강의 개요
- 강의 번호: `20`
- 모듈: `Module E / OpenStack Operations`
- 난이도: `advanced`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- 1~19강 내용을 하나의 운영 Runbook으로 통합한다.
- 점검/배포/복구 시나리오를 재현 가능한 절차로 정리한다.
- 실무 적용 가능한 자동화 문서 품질 기준을 완성한다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. 강의별 핵심 체크리스트를 통합한다.
2. 강의 playbook을 install_enabled=false/true 각각 실행한다.
3. 결과 로그를 기반으로 최종 Runbook을 작성한다.
4. 실패 시나리오 2개 이상에 대한 대응 절차를 정리한다.
5. 최종 회고와 개선 우선순위를 문서화한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행 (설치 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lecture20/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture20/playbook.yml -e install_enabled=true

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
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=lecture20+openstack+ansible)

