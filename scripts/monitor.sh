#!/bin/bash

LOG_FILE="openstack_dashboard.md"

# 초기화
echo "# 🚀 OpenStack 설치 상태 대시보드" > $LOG_FILE
echo "" >> $LOG_FILE
echo "업데이트 시간: $(date '+%Y-%m-%d %H:%M:%S')" >> $LOG_FILE
echo "" >> $LOG_FILE

# 패키지 목록
PACKAGES=("keystone" "glance" "nova" "neutron" "placement")

# 상태 기록 함수
check_package() {
    local pkg=$1
    if dpkg -l | grep -q $pkg; then
        echo "- [x] $pkg ✅ 설치됨" >> $LOG_FILE
    else
        echo "- [ ] $pkg ❌ 미설치" >> $LOG_FILE
    fi
}

# 모든 패키지 확인
for pkg in "${PACKAGES[@]}"; do
    check_package $pkg
done
