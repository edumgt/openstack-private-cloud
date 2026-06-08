#!/bin/bash
source /home/ubuntu/admin-openrc
set -e

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
info() { echo -e "${YELLOW}[>>]${NC} $1"; }
err()  { echo -e "${RED}[ERR]${NC} $1"; exit 1; }

echo "========================================"
echo "  OpenStack Lab Resource Initializer"
echo "========================================"

# ── 1. CirrOS 이미지 다운로드 & 업로드 ──────────────────────────
info "CirrOS 이미지 확인..."
if openstack image show cirros 2>/dev/null | grep -q "active"; then
    ok "cirros 이미지 이미 존재"
else
    CIRROS_VER="0.6.2"
    CIRROS_URL="https://download.cirros-cloud.net/${CIRROS_VER}/cirros-${CIRROS_VER}-x86_64-disk.img"
    CIRROS_FILE="/tmp/cirros-${CIRROS_VER}.img"

    info "CirrOS ${CIRROS_VER} 다운로드 중..."
    curl -L -o "$CIRROS_FILE" "$CIRROS_URL" --progress-bar || \
        err "다운로드 실패. 네트워크 확인 필요"

    info "Glance에 이미지 업로드..."
    openstack image create "cirros" \
        --file "$CIRROS_FILE" \
        --disk-format qcow2 \
        --container-format bare \
        --public \
        --property os_type=linux \
        --property hw_rng_model=virtio
    ok "CirrOS 이미지 업로드 완료"
    rm -f "$CIRROS_FILE"
fi

# ── 2. Flavor 생성 ────────────────────────────────────────────────
info "Flavor 생성..."
for flavor_def in \
    "m1.nano   1  64    1" \
    "m1.tiny   1  512   1" \
    "m1.small  1  2048  20" \
    "m1.medium 2  4096  40"
do
    name=$(echo $flavor_def | awk '{print $1}')
    vcpu=$(echo $flavor_def | awk '{print $2}')
    ram=$(echo $flavor_def | awk '{print $3}')
    disk=$(echo $flavor_def | awk '{print $4}')

    if openstack flavor show "$name" 2>/dev/null | grep -q "name"; then
        ok "flavor ${name} 이미 존재"
    else
        openstack flavor create "$name" \
            --vcpus "$vcpu" --ram "$ram" --disk "$disk" --public
        ok "flavor ${name} 생성 (${vcpu}vCPU / ${ram}MB RAM / ${disk}GB)"
    fi
done

# ── 3. 네트워크 생성 (provider flat + tenant vxlan) ──────────────
info "Provider 외부 네트워크 생성..."
if ! openstack network show external 2>/dev/null | grep -q "name"; then
    openstack network create external \
        --provider-physical-network provider \
        --provider-network-type flat \
        --external \
        --share
    openstack subnet create external-subnet \
        --network external \
        --subnet-range 10.0.1.0/24 \
        --allocation-pool start=10.0.1.100,end=10.0.1.200 \
        --gateway 10.0.1.1 \
        --no-dhcp \
        --dns-nameserver 8.8.8.8
    ok "external 네트워크/서브넷 생성"
else
    ok "external 네트워크 이미 존재"
fi

info "내부 tenant 네트워크 생성..."
if ! openstack network show internal 2>/dev/null | grep -q "name"; then
    openstack network create internal
    openstack subnet create internal-subnet \
        --network internal \
        --subnet-range 192.168.100.0/24 \
        --gateway 192.168.100.1 \
        --dns-nameserver 8.8.8.8
    ok "internal 네트워크/서브넷 생성"
else
    ok "internal 네트워크 이미 존재"
fi

info "Router 생성..."
if ! openstack router show lab-router 2>/dev/null | grep -q "name"; then
    openstack router create lab-router
    openstack router set lab-router --external-gateway external
    openstack router add subnet lab-router internal-subnet
    ok "lab-router 생성 및 연결"
else
    ok "lab-router 이미 존재"
fi

# ── 4. Security Group 기본 룰 ─────────────────────────────────────
info "default security group에 ICMP/SSH 허용 룰 추가..."
DEFAULT_SG=$(openstack security group list --project admin -f value -c ID | head -1)
if [ -n "$DEFAULT_SG" ]; then
    openstack security group rule create "$DEFAULT_SG" \
        --protocol tcp --dst-port 22 --remote-ip 0.0.0.0/0 2>/dev/null \
        && ok "SSH(22) 룰 추가" || ok "SSH 룰 이미 존재"
    openstack security group rule create "$DEFAULT_SG" \
        --protocol icmp --remote-ip 0.0.0.0/0 2>/dev/null \
        && ok "ICMP 룰 추가" || ok "ICMP 룰 이미 존재"
    openstack security group rule create "$DEFAULT_SG" \
        --protocol tcp --dst-port 80 --remote-ip 0.0.0.0/0 2>/dev/null \
        && ok "HTTP(80) 룰 추가" || ok "HTTP 룰 이미 존재"
fi

# ── 5. SSH Keypair 생성 ───────────────────────────────────────────
info "SSH Keypair 생성..."
if ! openstack keypair show lab-key 2>/dev/null | grep -q "name"; then
    ssh-keygen -t rsa -b 2048 -f /home/ubuntu/.ssh/lab-key -N "" -q
    openstack keypair create lab-key \
        --public-key /home/ubuntu/.ssh/lab-key.pub
    ok "lab-key keypair 생성 (/home/ubuntu/.ssh/lab-key)"
else
    ok "lab-key 이미 존재"
fi

# ── 6. 최종 요약 ─────────────────────────────────────────────────
echo ""
echo "========================================"
echo "  리소스 현황"
echo "========================================"
echo "[이미지]"
openstack image list --format table
echo ""
echo "[Flavor]"
openstack flavor list --format table
echo ""
echo "[네트워크]"
openstack network list --format table
echo ""
echo "[Keypair]"
openstack keypair list --format table
echo ""
echo "[Security Group]"
openstack security group list --format table
echo ""
ok "초기화 완료! Horizon에서 인스턴스 생성 가능합니다."
echo "  Flavor:  m1.nano (1vCPU/64MB/1GB) — CirrOS 전용"
echo "  Image:   cirros"
echo "  Network: internal (192.168.100.0/24)"
echo "  Keypair: lab-key"
