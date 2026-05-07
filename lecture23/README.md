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
- `./lecture.yml`
- `./playbook.yml`

## 10. 추가 학습 자료
- OpenStack Swift 공식 문서: https://docs.openstack.org/swift/latest/
- Swift vs S3 비교
- Object Storage 모범 사례

## 유튜브 영상 찾아보기
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=lecture23+openstack+ansible)

