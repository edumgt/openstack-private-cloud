# 02. Inventory / Variables / Facts

## 1) Inventory(인벤토리)
- `ansible/inventories/local/hosts.ini` : localhost
- `ansible/inventories/docker/hosts.ini` : 원격 docker 호스트용(예시)
- `ansible/inventories/aws/aws_ec2.yml` : AWS Dynamic Inventory

## 2) 변수(Variables)
Ansible 변수는 우선순위(Precedence)가 있습니다.
학습 단계에서는 아래만 기억해도 충분합니다.

- `-e key=value` (가장 강력)
- `ansible/group_vars/all.yml` (공통)
- `host_vars/<host>.yml` (호스트별)
- playbook vars / role defaults

## 3) Facts
Ansible는 기본적으로 타겟의 정보를 수집합니다.
```bash
ansible -i ansible/inventories/local/hosts.ini local -m setup | head
```

## 4) 조건문/반복문 맛보기
- `when:` 으로 OS별 분기
- `loop:` 로 여러 항목 반복

예시는 `ansible/roles/common/tasks/main.yml`에서 확인하세요.

## 유튜브 영상 찾아보기
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=openstack+ansible+inventory+vars)

