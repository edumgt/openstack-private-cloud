# 강의별 실습 가이드 (lecture01 ~ lecture24)

---

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
- `lecture01/lecture.yml`
- `lecture01/playbook.yml`

---

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
- `lecture02/lecture.yml`
- `lecture02/playbook.yml`

---

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
- `lecture03/lecture.yml`
- `lecture03/playbook.yml`

---

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
- `lecture04/lecture.yml`
- `lecture04/playbook.yml`

---

# lecture05 - Role 분리와 재사용 설계

## 1. 강의 개요
- 강의 번호: `05`
- 모듈: `Module A / Ansible Foundation`
- 난이도: `beginner`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- role 구조(tasks/defaults/handlers/templates) 책임을 분리한다.
- 같은 role을 여러 환경에서 재사용하는 변수 설계를 익힌다.
- 역할별 테스트 포인트를 정의한다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. roles 디렉토리 구조를 검토한다.
2. reference playbook으로 role 호출 패턴을 확인한다.
3. 강의 playbook 실행으로 기본 루틴을 검증한다.
4. install_enabled=true 재실행으로 설치/검증 흐름을 확인한다.
5. 재사용 체크리스트를 작성한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행 (설치 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lecture05/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture05/playbook.yml -e install_enabled=true

# 레퍼런스 플레이북 실행
ansible-playbook -i ansible/inventories/local/hosts.ini ansible/playbooks/03_role_web.yml
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
- `lecture05/lecture.yml`
- `lecture05/playbook.yml`

---

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
- `lecture06/lecture.yml`
- `lecture06/playbook.yml`

---

# lecture07 - 사용자/권한/SSH 정책 자동화

## 1. 강의 개요
- 강의 번호: `07`
- 모듈: `Module B / Ansible Operations`
- 난이도: `beginner`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- 서버 계정/권한/SSH 정책 표준화를 자동화한다.
- 운영 보안 기본 정책을 playbook 태스크로 정의한다.
- 권한 변경 시 검증 포인트를 정리한다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. reference users playbook 흐름을 확인한다.
2. 강의 playbook 실행으로 공통 루틴을 검증한다.
3. install_enabled=true에서 설치 태스크를 함께 확인한다.
4. 권한 관련 태스크 점검 포인트를 문서화한다.
5. 재실행 후 변화량을 비교한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행 (설치 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lecture07/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture07/playbook.yml -e install_enabled=true

# 레퍼런스 플레이북 실행
ansible-playbook -i ansible/inventories/local/hosts.ini ansible/playbooks/01_users.yml
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
- `lecture07/lecture.yml`
- `lecture07/playbook.yml`

---

# lecture08 - Nginx 서비스 배포와 검증

## 1. 강의 개요
- 강의 번호: `08`
- 모듈: `Module B / Ansible Operations`
- 난이도: `beginner`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- Nginx 설치/설정/상태 확인 절차를 자동화한다.
- 서비스 배포 후 헬스체크 기준을 학습한다.
- 구성 변경 시 rollback 관점을 정리한다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. reference nginx playbook을 실행한다.
2. 강의 playbook으로 공통 검증 루틴을 실행한다.
3. install_enabled=true로 패키지 설치 경로를 확인한다.
4. 서비스 상태 점검 명령을 로그로 남긴다.
5. 문제 발생 시 재시작/설정 검증 순서를 기록한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행 (설치 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lecture08/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture08/playbook.yml -e install_enabled=true

# 레퍼런스 플레이북 실행
ansible-playbook -i ansible/inventories/local/hosts.ini ansible/playbooks/02_nginx.yml
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
- `lecture08/lecture.yml`
- `lecture08/playbook.yml`

---

# lecture09 - Docker Engine 설치 자동화

## 1. 강의 개요
- 강의 번호: `09`
- 모듈: `Module B / Ansible Operations`
- 난이도: `intermediate`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- Docker 엔진 설치/버전 점검 태스크 흐름을 이해한다.
- 운영 서버 표준 패키지 설치 절차를 정형화한다.
- 컨테이너 런타임 설치 후 기본 진단 명령을 익힌다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. reference docker engine playbook을 실행한다.
2. 강의 playbook으로 공통 진단 태스크를 수행한다.
3. install_enabled=true에서 docker 설치 여부를 확인한다.
4. docker version 결과를 로그에 기록한다.
5. 재실행 후 상태 변화를 점검한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행 (설치 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lecture09/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture09/playbook.yml -e install_enabled=true

# 레퍼런스 플레이북 실행
ansible-playbook -i ansible/inventories/local/hosts.ini ansible/playbooks/10_docker_engine_install.yml
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
- `lecture09/lecture.yml`
- `lecture09/playbook.yml`

---

# lecture10 - Compose 배포와 업데이트 전략

## 1. 강의 개요
- 강의 번호: `10`
- 모듈: `Module B / Ansible Operations`
- 난이도: `intermediate`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- Compose 기반 멀티서비스 배포 흐름을 이해한다.
- 업데이트 전략(rolling/blue-green) 연결 포인트를 학습한다.
- 배포 후 검증/롤백 기준을 정리한다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. reference stack deploy playbook을 실행한다.
2. 강의 playbook으로 공통 루틴을 점검한다.
3. install_enabled=true로 의존 패키지 설치 상태를 확인한다.
4. 배포 결과 점검 체크리스트를 작성한다.
5. 운영 반영 전 검증 순서를 정리한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행 (설치 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lecture10/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture10/playbook.yml -e install_enabled=true

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
- `lecture10/lecture.yml`
- `lecture10/playbook.yml`

---

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
- `lecture11/lecture.yml`
- `lecture11/playbook.yml`

---

# lecture12 - AWS VPC/EC2 기본 자동화 브릿지

## 1. 강의 개요
- 강의 번호: `12`
- 모듈: `Module C / Cloud Bridge`
- 난이도: `intermediate`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- VPC/EC2 리소스 자동화 흐름을 개념적으로 이해한다.
- IaaS 리소스 모델을 OpenStack과 매핑한다.
- 실습 전후 자원 정리 중요성을 학습한다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. reference VPC playbook을 검토한다.
2. 강의 playbook 실행으로 표준 루틴을 확인한다.
3. install_enabled=true에서 설치 결과를 점검한다.
4. VPC-OpenStack 네트워크 매핑표를 만든다.
5. 실패 시 자격/리전/권한 점검 순서를 정리한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행 (설치 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lecture12/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture12/playbook.yml -e install_enabled=true

# 레퍼런스 플레이북 실행
ansible-playbook -i ansible/inventories/local/hosts.ini ansible/playbooks/20_aws_create_vpc.yml
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
- `lecture12/lecture.yml`
- `lecture12/playbook.yml`

---

# lecture13 - OpenStack 아키텍처와 핵심 서비스 이해

## 1. 강의 개요
- 강의 번호: `13`
- 모듈: `Module D / OpenStack Foundation`
- 난이도: `beginner`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- Keystone/Glance/Nova/Neutron/Cinder의 역할을 이해한다.
- API-DB-MQ-Worker 구조를 운영 관점으로 정리한다.
- 컴포넌트 간 연동 흐름을 도식화한다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. 기술 스택 요약을 읽고 구성요소를 정리한다.
2. 강의 playbook으로 실행 루틴을 검증한다.
3. install_enabled=true로 의존 도구 설치를 확인한다.
4. 컴포넌트 맵(역할/저장소/통신)을 문서화한다.
5. 다음 강의 인증 모델과 연결 포인트를 작성한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행 (설치 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lecture13/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture13/playbook.yml -e install_enabled=true

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
- `lecture13/lecture.yml`
- `lecture13/playbook.yml`

---

# lecture14 - Keystone 인증/프로젝트/역할 모델

## 1. 강의 개요
- 강의 번호: `14`
- 모듈: `Module D / OpenStack Foundation`
- 난이도: `intermediate`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- 토큰/프로젝트/사용자/역할 관계를 이해한다.
- 인증 실패 시 점검 항목을 정의한다.
- AWS IAM과 Keystone의 대응 관계를 정리한다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. 인증 모델 다이어그램을 작성한다.
2. 강의 playbook 실행으로 공통 검증 루틴을 수행한다.
3. install_enabled=true 실행 결과를 기록한다.
4. 권한 모델 비교표(AWS vs OpenStack)를 작성한다.
5. 운영 체크포인트를 정리한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행 (설치 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lecture14/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture14/playbook.yml -e install_enabled=true

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
- `lecture14/lecture.yml`
- `lecture14/playbook.yml`

---

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
- `lecture15/lecture.yml`
- `lecture15/playbook.yml`

---

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
- `lecture16/lecture.yml`
- `lecture16/playbook.yml`

---

# lecture17 - Neutron/Cinder 리소스 자동화

## 1. 강의 개요
- 강의 번호: `17`
- 모듈: `Module D / OpenStack Foundation`
- 난이도: `intermediate`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- Neutron 네트워크/서브넷/라우터/FIP 개념을 정리한다.
- Cinder 볼륨 생성/연결/분리 흐름을 이해한다.
- 네트워크/스토리지 운영 기준 체크리스트를 만든다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. Neutron 구성요소와 에이전트 역할을 정리한다.
2. 강의 playbook 실행으로 검증 루틴을 수행한다.
3. install_enabled=true 결과를 확인한다.
4. 볼륨 라이프사이클 표를 작성한다.
5. 운영 점검 항목을 정리한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 기본 검증 실행 (설치 제외)
ansible-playbook -i ansible/inventories/local/hosts.ini lecture17/playbook.yml -e install_enabled=false

# 설치 포함 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture17/playbook.yml -e install_enabled=true

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
- `lecture17/lecture.yml`
- `lecture17/playbook.yml`

---

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
- `lecture18/lecture.yml`
- `lecture18/playbook.yml`

---

# lecture19 - 실제 OpenStack 클라이언트 환경 준비

## 1. 강의 개요
- 강의 번호: `19`
- 모듈: `Module E / OpenStack Operations`
- 난이도: `intermediate`
- 권장 시간: `60분`

## 2. 상세 학습 내용
- 실제 OpenStack API에 연결할 클라이언트 환경을 준비한다.
- `openrc`와 `clouds.yaml`을 생성한다.
- 별도 Ubuntu 서버에 `DevStack`을 올릴 수 있도록 사전 준비를 수행한다.

## 3. 실행 전 체크
- Python/Ansible 버전 확인
- 실제 OpenStack API 또는 DevStack 설치 대상 Ubuntu 서버 준비
- 인벤토리 파일 확인: `ansible/inventories/dev/hosts.ini`
- 필요 시 `sudo` 권한 확인

## 4. 실습 절차
1. OpenStack 인증 환경 변수 또는 실제 API 주소를 준비한다.
2. `lecture19/playbook.yml`로 `real-openstack-openrc`와 `clouds.yaml`을 만든다.
3. 별도 서버가 있으면 `ansible/playbooks/30_devstack_host_prep.yml`로 DevStack 설치 준비를 한다.
4. `stack.sh` 실행 후 Keystone URL을 확인한다.
5. `lecture20`, `lecture21`로 검증을 이어간다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 실제 OpenStack 클라이언트 환경 준비
export OS_AUTH_URL=http://<REAL_OPENSTACK_IP>:5000/v3
export OS_USERNAME=admin
export OS_PASSWORD=<PASSWORD>
export OS_PROJECT_NAME=admin

ansible-playbook -i ansible/inventories/local/hosts.ini lecture19/playbook.yml -e install_enabled=true

# 별도 Ubuntu 서버에 DevStack 설치 준비
ansible-playbook -i ansible/inventories/dev/hosts.ini ansible/playbooks/30_devstack_host_prep.yml -l openstack_hosts

# 대상 서버에서 DevStack 실제 설치
sudo -iu stack bash -lc 'cd /opt/devstack/devstack && ./stack.sh'
```

## 6. 결과 확인 기준
- `PLAY RECAP` 기준 `failed=0`
- `.lab/real-openstack-openrc` 생성 확인
- `/root/.config/openstack/clouds.yaml` 생성 확인
- DevStack 서버에 `/opt/devstack/devstack/local.conf` 생성 확인
- DevStack 설치 후 `http://<server-ip>:5000/v3` 응답 확인

## 7. 트러블슈팅 힌트
- WSL2 로컬 머신은 실제 OpenStack 제어면 호스트로 비권장
- DevStack은 별도 Ubuntu 서버(권장 8 vCPU / 16GB RAM 이상)에서 실행
- `5000/tcp` timeout: 방화벽, 라우팅, DevStack `stack.sh` 로그 확인
- `openstack token issue` 실패: `real-openstack-openrc` 값과 Keystone 상태 확인

## 8. 참고 파일
- `lecture19/lecture.yml`
- `lecture19/playbook.yml`
- `ansible/playbooks/30_devstack_host_prep.yml`

---

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
- `lecture20/lecture.yml`
- `lecture20/playbook.yml`

---

# lecture21 - OpenStack/Nova 기본 점검

## 1. 강의 개요
- 강의 번호: `21`
- 모듈: `Module E / OpenStack Operations`
- 난이도: `intermediate`
- 권장 시간: `30분`

## 2. 상세 학습 내용
- `openstack` CLI로 Keystone 인증이 되는지 확인한다.
- `nova service list`와 `hypervisor list`를 조회한다.
- `compute1`, `compute2`를 동적 인벤토리로 등록한다.
- 두 서버에 `nginx`를 설치하고 80 포트 HTTP 응답을 확인한다.
- Codespaces mock 환경과 실제 OpenStack 환경을 같은 플레이북으로 점검한다.

## 3. 실행 전 체크
- `lecture22`를 먼저 실행해 mock 환경 또는 인증 정보를 준비
- `.venv/bin/openstack` 설치 여부 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`
- mock 환경 기본 인증 엔드포인트는 `http://127.0.0.1:15000/v3`
- 실제 OpenStack에서는 `compute1`, `compute2`에 SSH 가능해야 함
- 보안 그룹 또는 방화벽에서 `22/tcp`, `80/tcp` 허용 필요
- 기본값은 floating IP 우선이며, floating IP가 없으면 SSH 배포를 중단함
- 필요 시 `OPENSTACK_SSH_KEY_PATH` 또는 `-e compute_ssh_private_key_file=...` 지정
- `lecture22` mock openrc를 사용하면 OpenStack 조회까지만 수행하고, 원격 `nginx` 배포는 자동으로 건너뜀

## 4. 실습 절차
1. Keystone 엔드포인트 응답을 확인한다.
2. `openstack token issue` 결과를 확인한다.
3. `openstack compute service list` 결과를 기록한다.
4. `openstack hypervisor list` 결과를 기록한다.
5. `compute1`, `compute2`의 접속 IP를 식별한다.
6. 두 서버에 `nginx`를 설치하고 서비스 기동을 확인한다.
7. 각 서버의 `http://<ip>:80` 접속 결과를 확인한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# lecture22 이후 실행
source .lab/keystone-admin-openrc
ansible-playbook -i ansible/inventories/local/hosts.ini lecture21/playbook.yml -e install_enabled=false

# lecture21에서 필요한 패키지까지 같이 준비
ansible-playbook -i ansible/inventories/local/hosts.ini lecture21/playbook.yml -e install_enabled=true

# SSH 사용자/키를 함께 지정하는 예시
ansible-playbook -i ansible/inventories/local/hosts.ini lecture21/playbook.yml \
  -e install_enabled=false \
  -e compute_ssh_user=ubuntu \
  -e compute_ssh_private_key_file=~/.ssh/openstack.pem

# floating IP 대신 직접 접속 가능한 IP를 강제로 지정하는 예시
ansible-playbook -i ansible/inventories/local/hosts.ini lecture21/playbook.yml \
  -e install_enabled=false \
  -e 'compute_access_ip_overrides={"compute1":"192.168.0.101","compute2":"192.168.0.102"}'
```

### 5.1 실제 OpenStack openrc 파일이 없을 때
```bash
export OS_AUTH_URL=http://<OPENSTACK_IP>:5000/v3
export OS_USERNAME=admin
export OS_PASSWORD=<PASSWORD>
export OS_PROJECT_NAME=admin
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_DOMAIN_NAME=Default
export OS_REGION_NAME=RegionOne
export OS_INTERFACE=public
export OS_IDENTITY_API_VERSION=3

bash scripts/create_real_openrc.sh "$PWD"
source .lab/real-openstack-openrc
```

그 다음 실제 OpenStack에서 `floating IP`를 붙이고 배포합니다.

```bash
openstack floating ip create public
openstack server add floating ip compute1 <FLOATING_IP_1>
openstack floating ip create public
openstack server add floating ip compute2 <FLOATING_IP_2>

.venv/bin/ansible-playbook \
  -i ansible/inventories/local/hosts.ini \
  lecture21/playbook.yml \
  -e openrc_path="$PWD/.lab/real-openstack-openrc" \
  -e compute_ssh_user=ubuntu \
  -e compute_ssh_private_key_file=~/.ssh/openstack.pem
```

## 6. 결과 확인 기준
- `PLAY RECAP` 기준 `failed=0`
- `token_rc=0`
- `nova_service_rc=0`
- `hypervisor_rc=0`
- 서비스/하이퍼바이저 목록이 출력됨
- `compute1`, `compute2`에 `nginx`가 설치되고 서비스가 실행됨
- 제어 노드에서 `http://<compute-access-ip>:80` 확인 시 `200` 응답
- 단, 위 배포 결과 검증은 실제 OpenStack 인증 정보 사용 시에만 해당

## 7. 트러블슈팅 힌트
- `openstack` 명령 없음: `lecture22`를 `install_enabled=true`로 다시 실행
- `keystone_http_status`가 `200`이 아님: mock 서버 또는 실제 Keystone 상태 확인
- Nova 조회 실패: 인증 정보 또는 compute endpoint 확인
- SSH 연결 실패: `compute_ssh_user`, 개인키 경로, security group의 `22/tcp` 허용 확인
- `10.x.x.x` 같은 fixed IP timeout: tenant 내부망만 붙어 있는 상태일 수 있으니 floating IP 연결 또는 `compute_access_ip_overrides` 사용
- HTTP 80 실패: 인스턴스 security group의 `80/tcp` 허용 여부와 `nginx` 서비스 상태 확인
- mock 환경은 floating IP/SSH 대상이 없으므로 실제 SSH/nginx 배포 검증은 실제 OpenStack 인스턴스에서 수행

## 8. 참고 파일
- `lecture21/lecture.yml`
- `lecture21/playbook.yml`
- `lecture22/playbook.yml`

---

# lecture22 - Codespaces용 Keystone/Nova Mock 준비

## 1. 강의 개요
- 강의 번호: `22`
- 모듈: `Module E / OpenStack Operations`
- 난이도: `intermediate`
- 권장 시간: `30분`

## 2. 상세 학습 내용
- Codespaces에서 `ansible-core`와 `python-openstackclient`를 준비한다.
- 로컬 mock Keystone/Nova API를 실행한다.
- `lecture21`에서 재사용할 `openrc` 파일을 생성한다.
- 기존 Apache/Keystone와 충돌하지 않도록 mock API는 `15000~15004` 중 사용 가능한 포트를 자동 선택한다.
- 브라우저에서 상태를 볼 수 있도록 Horizon-style dashboard를 함께 제공한다.

## 3. 실행 전 체크
- Codespaces 또는 devcontainer 환경 진입
- 프로젝트 루트에서 `.venv` 활성화 여부 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`

## 4. 실습 절차
1. `install_enabled=true`로 Python 패키지를 준비한다.
2. mock Keystone/Nova 서버를 실행한다.
3. `.lab/keystone-admin-openrc` 파일을 생성한다.
4. `openstack token issue`가 성공하는지 확인한다.
5. `lecture21`을 실행해 Nova 서비스/하이퍼바이저 조회까지 확인한다.
6. `/dashboard` 페이지에서 웹 상태 화면을 확인한다.

## 5. 실행 방법 (프로젝트 루트에서 실행)
```bash
# 1) Codespaces 기본 준비
bash .devcontainer/post-create.sh

# 2) lecture22 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture22/playbook.yml -e install_enabled=true

# 3) 인증 정보 적용
source .lab/keystone-admin-openrc

# 4) dashboard 확인
echo "$OS_AUTH_URL"   # 예: http://127.0.0.1:15000/v3
# 브라우저에서 http://127.0.0.1:15000/dashboard 접속

# 5) lecture21 실행
ansible-playbook -i ansible/inventories/local/hosts.ini lecture21/playbook.yml -e install_enabled=false
```

## 6. 결과 확인 기준
- `PLAY RECAP` 기준 `failed=0`
- `.venv/bin/openstack --version` 출력 정상
- 선택된 포트의 `/healthz` 응답 정상
- `.lab/keystone-admin-openrc` 파일 생성 확인
- 선택된 포트의 `/dashboard` 페이지 접속 정상

## 7. 트러블슈팅 힌트
- `openstack` 명령 없음: `bash .devcontainer/post-create.sh` 또는 `install_enabled=true` 재실행
- mock 포트 충돌: `.lab/openstack-mock/server.pid` 확인 후 `scripts/stop_mock_openstack.sh` 실행
- mock 서버 비정상: `.lab/openstack-mock/server.log` 확인

## 8. 참고 파일
- `lecture22/lecture.yml`
- `lecture22/playbook.yml`
- `scripts/mock_openstack_api.py`

---

# lecture23 - Swift Object Storage 점검

## 1. 강의 개요
- 강의 번호: `23`
- 모듈: `Module E / OpenStack Operations`
- 난이도: `intermediate`
- 권장 시간: `40분`

## 2. 상세 학습 내용
- Swift Object Storage 서비스 개념을 이해한다.
- 공용 "파일 저장소" 역할을 확인한다. (공유 디스크/공유 폴더와는 다름)
- Container와 Object 구조를 이해한다.
- Swift CLI로 파일 업로드/다운로드를 테스트한다.
- S3 호환 API와의 차이점을 정리한다.

## 3. Swift vs. 공유 디스크/폴더
- **Swift**: HTTP REST API 기반 Object Storage
  - URL로 접근 가능한 파일 저장소
  - 확장 가능한 분산 스토리지
  - 메타데이터 기반 관리
  - 버전 관리 지원
- **공유 디스크/폴더** (예: NFS, CIFS):
  - 파일 시스템 기반 접근
  - 마운트 필요
  - POSIX 호환

## 4. 실행 전 체크
- Python/Ansible 버전 확인
- OpenStack 인증 정보 (실제 환경 또는 Mock)
- Swift 서비스 설치 여부 확인
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`

## 5. 실습 절차
1. Swift 서비스 endpoint 확인
2. Container 생성 (`openstack container create`)
3. Object 업로드 (`openstack object create`)
4. Object 목록 조회 (`openstack object list`)
5. Object 다운로드 (`openstack object save`)
6. Object 삭제 및 Container 정리

## 6. 실행 방법 (프로젝트 루트에서 실행)

### 6.1 실제 OpenStack 환경
```bash
# Swift 서비스 확인
source .lab/real-openstack-openrc
.venv/bin/openstack service list | grep object-store

# lecture23 실행 (Swift가 설치된 경우)
.venv/bin/ansible-playbook -i ansible/inventories/local/hosts.ini \
  lecture23/playbook.yml \
  -e install_enabled=false \
  -e openrc_path=.lab/real-openstack-openrc \
  -e use_mock_openstack_auth=false
```

### 6.2 Mock 환경 (Swift 미설치 시)
```bash
# Mock 환경에서 개념 학습
.venv/bin/ansible-playbook -i ansible/inventories/local/hosts.ini \
  lecture23/playbook.yml \
  -e install_enabled=false \
  -e swift_service_available=false
```

## 7. 결과 확인 기준
- `PLAY RECAP` 기준 `failed=0`
- Swift 서비스 설치 시:
  - Container 생성 성공
  - Object 업로드 성공
  - Object 조회 및 다운로드 성공
- Swift 미설치 시:
  - 서비스 부재 확인
  - 대체 방안 안내 (S3, MinIO 등)

## 8. 트러블슈팅 힌트
- Swift 서비스 없음: `service list`에서 `object-store` 확인
- 권한 오류: project role 확인 (`openstack role assignment list`)
- Container 생성 실패: quota 확인

## 9. 참고 파일
- `lecture23/lecture.yml`
- `lecture23/playbook.yml`

## 10. 추가 학습 자료
- OpenStack Swift 공식 문서: https://docs.openstack.org/swift/latest/
- Swift vs S3 비교
- Object Storage 모범 사례

---

# lecture24 - Octavia Load Balancer 점검

## 1. 강의 개요
- 강의 번호: `24`
- 모듈: `Module E / OpenStack Operations`
- 난이도: `intermediate`
- 권장 시간: `50분`

## 2. 상세 학습 내용
- Octavia Load Balancer as a Service (LBaaS) 개념을 이해한다.
- 두 compute 또는 그 위 VM 서비스들을 하나의 진입점으로 묶는 방법을 학습한다.
- Load Balancer, Listener, Pool, Member 구조를 이해한다.
- Health Monitor로 자동 장애 조치를 구성한다.
- 실제 트래픽 분산 시나리오를 테스트한다.

## 3. Octavia 사용 사례
- **웹 서비스 HA**: 여러 웹 서버를 하나의 VIP로 묶기
- **API Gateway**: 마이크로서비스 앞단 부하 분산
- **Compute 이중화**: compute1, compute2를 단일 진입점으로 통합
- **자동 장애 조치**: Health check로 장애 서버 자동 제외

## 4. 실행 전 체크
- Python/Ansible 버전 확인
- OpenStack 인증 정보 (실제 환경 또는 Mock)
- Octavia 서비스 설치 여부 확인
- Neutron 네트워크 존재 확인
- 최소 2대의 compute 인스턴스 또는 테스트 VM 필요
- 인벤토리 파일 확인: `ansible/inventories/local/hosts.ini`

## 5. 실습 절차
1. Octavia 서비스 endpoint 확인
2. Load Balancer 생성 (`openstack loadbalancer create`)
3. Listener 추가 (포트 80 HTTP)
4. Pool 생성 (Round Robin 알고리즘)
5. Member 추가 (compute1, compute2의 private IP)
6. Health Monitor 설정
7. VIP(Virtual IP)로 트래픽 테스트
8. 한 서버 중지 후 자동 장애 조치 확인

## 6. 실행 방법 (프로젝트 루트에서 실행)

### 6.1 실제 OpenStack 환경
```bash
# Octavia 서비스 확인
source .lab/real-openstack-openrc
.venv/bin/openstack service list | grep load-balancer

# lecture24 실행 (Octavia가 설치된 경우)
.venv/bin/ansible-playbook -i ansible/inventories/local/hosts.ini \
  lecture24/playbook.yml \
  -e install_enabled=false \
  -e openrc_path=.lab/real-openstack-openrc \
  -e use_mock_openstack_auth=false \
  -e lb_vip_subnet=private-subnet
```

### 6.2 Mock 환경 (Octavia 미설치 시)
```bash
# Mock 환경에서 개념 학습
.venv/bin/ansible-playbook -i ansible/inventories/local/hosts.ini \
  lecture24/playbook.yml \
  -e install_enabled=false \
  -e octavia_service_available=false
```

## 7. Load Balancer 구성 요소
```
Load Balancer
  └─ Listener (포트 80)
       └─ Pool (Round Robin)
            ├─ Member: compute1 (10.0.0.11:80)
            ├─ Member: compute2 (10.0.0.12:80)
            └─ Health Monitor (HTTP GET /)
```

## 8. 결과 확인 기준
- `PLAY RECAP` 기준 `failed=0`
- Octavia 서비스 설치 시:
  - Load Balancer 생성 성공
  - VIP 할당 성공
  - 트래픽 분산 확인 (compute1, compute2 번갈아 응답)
  - Health check 동작 확인
- Octavia 미설치 시:
  - 서비스 부재 확인
  - 대체 방안 안내 (HAProxy, Nginx 등)

## 9. 트러블슈팅 힌트
- Octavia 서비스 없음: `service list`에서 `load-balancer` 확인
- Amphora 이미지 없음: amphora-x64-haproxy 이미지 확인
- Member 추가 실패: 서브넷 및 보안 그룹 확인
- VIP 접근 불가: floating IP 연결 확인

## 10. 참고 파일
- `lecture24/lecture.yml`
- `lecture24/playbook.yml`

## 11. 추가 학습 자료
- OpenStack Octavia 공식 문서: https://docs.openstack.org/octavia/latest/
- Amphora 구조 이해
- Load Balancing 알고리즘 (Round Robin, Least Connections, Source IP)
