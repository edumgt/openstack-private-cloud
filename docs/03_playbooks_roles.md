# 03. Playbook / Role 구조

## Playbook
- 어떤 호스트에
- 어떤 작업을
- 어떤 순서로 적용할지 정의

예: `ansible/playbooks/02_nginx.yml`

## Role
반복되는 작업을 폴더 구조로 정리한 단위입니다.

- ansible/roles/webserver : Nginx 설치 + index.html 템플릿 배포
- ansible/roles/docker_engine : Docker 엔진 설치
- ansible/roles/common : 공통 유틸/기본 설정

Role 실행 예시:
```bash
ansible-playbook ansible/playbooks/03_role_web.yml
```

## 유튜브 영상 찾아보기
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=openstack+ansible+playbooks+roles)

