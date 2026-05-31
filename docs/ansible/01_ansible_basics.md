# Ansible 기초(초급)

## 핵심 개념
- **Inventory(인벤토리)**: 대상 서버 목록과 그룹
- **Playbook**: 어떤 그룹에 어떤 작업을 어떤 순서로 할지
- **Module**: 파일 복사, 패키지 설치, 서비스 제어 같은 작업 단위
- **Idempotent(멱등성)**: 여러 번 실행해도 결과가 같도록 작성

## 자주 쓰는 명령

```bash
# ping
ansible -i ansible/inventories/dev/hosts.ini all -m ping

# 특정 그룹에서 명령 실행
ansible -i ansible/inventories/dev/hosts.ini app_hosts -a "uname -a"

# 플레이북 실행
ansible-playbook -i ansible/inventories/dev/hosts.ini ansible/playbooks/00_ping.yml
```

## 유튜브 영상 찾아보기
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=openstack+ansible+ansible+basics)

