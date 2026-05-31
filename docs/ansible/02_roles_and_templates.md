# Role / 템플릿 / 핸들러

## Role 구조
- `ansible/roles/<role>/tasks/main.yml` : 핵심 작업
- `ansible/roles/<role>/handlers/main.yml` : 서비스 재시작 같은 후속 작업
- `ansible/roles/<role>/templates/*.j2` : 설정 파일 템플릿

## 왜 Role을 쓰나?
- 플레이북을 짧고 읽기 쉽게 유지
- 재사용/표준화
- 환경(dev/stage/prod) 변수만 바꿔도 동일한 자동화

## 유튜브 영상 찾아보기
- [YouTube에서 관련 영상 검색하기](https://www.youtube.com/results?search_query=openstack+ansible+roles+and+templates)

