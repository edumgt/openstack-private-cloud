# Docker 운영 자동화

## 목표
- 서버 OS에 맞게 Docker 엔진을 설치/업데이트
- Compose 프로젝트를 배포
- 헬스체크로 정상 상태 확인

## 실행
```bash
ansible-playbook -i ansible/inventories/dev/hosts.ini ansible/playbooks/10_docker_engine_install.yml
ansible-playbook -i ansible/inventories/dev/hosts.ini ansible/playbooks/11_deploy_stack.yml
```

## 유튜브 영상 찾아보기
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=03+docker+with+ansible)

