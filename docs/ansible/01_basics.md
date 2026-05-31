# 01. Ansible 기초

## 핵심 개념
- **컨트롤 노드**: Ansible 명령을 실행하는 곳
- **관리 노드(타겟)**: 설정을 적용받는 서버
- **Inventory**: 관리 노드 목록
- **Module**: 실행 단위(예: ping, apt, user)
- **Playbook**: 작업을 순서대로 묶은 YAML
- **Idempotent**: 여러 번 실행해도 결과가 동일(중복 적용이 없어야 함)

## Ad-hoc 명령(한 줄 실행)
```bash
ansible -i ansible/inventories/local/hosts.ini local -m ping
ansible -i ansible/inventories/local/hosts.ini local -m command -a "uname -a"
```

## Playbook 실행
```bash
ansible-playbook ansible/playbooks/00_ping.yml
```

## Dry-run(미리보기)
```bash
ansible-playbook ansible/playbooks/02_nginx.yml --check --diff
```

## 유튜브 영상 찾아보기
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=openstack+ansible+basics)

