#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

TOKEN_ID = "mock-token"
IMAGE_ID = "f4f7b26d-2be8-4f10-9c95-9c3a7f6f51bf"
IMAGE2_ID = "a8c2e190-7b12-4e55-8a01-3e9f88d109aa"
SERVER_ID = "2f8cf7bb-1472-46f8-9f08-9f2a8d3e44cc"
SERVER2_ID = "7d7859f7-8f9e-4d64-bd8d-0e3bafe1f85f"
NETWORK1_ID = "a5f1b56f-9316-4b37-a89c-2e0e4b3e6cf7"
NETWORK2_ID = "b37a9f4c-6f0d-4d8f-9834-3bf21f99d365"
SUBNET1_ID = "c3a8d3e9-3d90-4a7a-9bc0-3df1739a6f4e"
SUBNET2_ID = "d4b0e7e3-bf26-4f6e-b0aa-8fbf1cd88b3a"
VOLUME1_ID = "8a40dcf7-4f14-4752-9f95-0a3f72fcde79"
VOLUME2_ID = "c9686048-2f6f-4e15-8ea4-95bcf65ba4d2"


def keystone_version_doc(host: str, keystone_port: int) -> dict:
    base = f"http://{host}:{keystone_port}/v3"
    return {
        "version": {
            "id": "v3.14",
            "status": "stable",
            "release": "2025.2 (Epoxy)",
            "links": [{"rel": "self", "href": base}],
            "media-types": [
                {
                    "base": "application/json",
                    "type": "application/vnd.openstack.identity-v3+json",
                }
            ],
        }
    }


def token_doc(host: str, keystone_port: int, nova_port: int) -> dict:
    return {
        "token": {
            "methods": ["password"],
            "expires_at": "2030-01-01T00:00:00Z",
            "project": {"id": "project-admin", "name": "admin", "domain": {"id": "default", "name": "Default"}},
            "user": {"id": "user-admin", "name": "admin", "domain": {"id": "default", "name": "Default"}},
            "catalog": [
                {
                    "id": "service-keystone",
                    "type": "identity",
                    "name": "keystone",
                    "endpoints": [
                        {
                            "id": "endpoint-keystone-public",
                            "interface": "public",
                            "region": "RegionOne",
                            "url": f"http://{host}:{keystone_port}/v3",
                        }
                    ],
                },
                {
                    "id": "service-nova",
                    "type": "compute",
                    "name": "nova",
                    "endpoints": [
                        {
                            "id": "endpoint-nova-public",
                            "interface": "public",
                            "region": "RegionOne",
                            "url": f"http://{host}:{keystone_port}/v2.1",
                        }
                    ],
                },
                {
                    "id": "service-glance",
                    "type": "image",
                    "name": "glance",
                    "endpoints": [
                        {
                            "id": "endpoint-glance-public",
                            "interface": "public",
                            "region": "RegionOne",
                            "url": f"http://{host}:{keystone_port}/v2",
                        }
                    ],
                },
                {
                    "id": "service-neutron",
                    "type": "network",
                    "name": "neutron",
                    "endpoints": [
                        {
                            "id": "endpoint-neutron-public",
                            "interface": "public",
                            "region": "RegionOne",
                            "url": f"http://{host}:{keystone_port}/v2.0",
                        }
                    ],
                },
                {
                    "id": "service-cinder",
                    "type": "volumev3",
                    "name": "cinderv3",
                    "endpoints": [
                        {
                            "id": "endpoint-cinder-public",
                            "interface": "public",
                            "region": "RegionOne",
                            "url": f"http://{host}:{keystone_port}/v3",
                        }
                    ],
                },
            ],
        }
    }


def mock_server_doc(
    server_id: str,
    name: str,
    network_name: str,
    fixed_ip: str,
    volume_id: str,
    host: str,
) -> dict:
    return {
        "id": server_id,
        "name": name,
        "status": "ACTIVE",
        "created": "2026-03-30T12:00:00Z",
        "updated": "2026-03-30T12:05:00Z",
        "flavor": {"id": "m1.small", "links": []},
        "image": {"id": IMAGE_ID, "links": []},
        "OS-EXT-SRV-ATTR:host": host,
        "addresses": {
            network_name: [
                {
                    "OS-EXT-IPS:type": "fixed",
                    "addr": fixed_ip,
                    "version": 4,
                }
            ]
        },
        "os-extended-volumes:volumes_attached": [{"id": volume_id}],
    }


def nova_servers_doc(name: str | None = None) -> dict:
    servers = [
        mock_server_doc(
            server_id=SERVER_ID,
            name="compute1",
            network_name="net-compute1",
            fixed_ip="10.10.1.11",
            volume_id=VOLUME1_ID,
            host="compute1",
        ),
        mock_server_doc(
            server_id=SERVER2_ID,
            name="compute2",
            network_name="net-compute2",
            fixed_ip="10.20.1.11",
            volume_id=VOLUME2_ID,
            host="compute2",
        ),
    ]
    if name:
        servers = [server for server in servers if server["name"] == name]
    return {"servers": servers}


def glance_versions_doc(host: str, keystone_port: int) -> dict:
    return {
        "versions": [
            {
                "id": "v2.8",
                "status": "CURRENT",
                "links": [{"rel": "self", "href": f"http://{host}:{keystone_port}/v2"}],
            }
        ]
    }


def glance_images_doc() -> dict:
    return {
        "images": [
            {
                "id": IMAGE_ID,
                "name": "ubuntu-24.04-noble",
                "status": "active",
                "disk_format": "qcow2",
                "container_format": "bare",
                "visibility": "public",
            },
            {
                "id": IMAGE2_ID,
                "name": "ubuntu-22.04",
                "status": "active",
                "disk_format": "qcow2",
                "container_format": "bare",
                "visibility": "public",
            },
        ]
    }


def glance_image_doc(image_id: str) -> tuple[int, dict]:
    for img in glance_images_doc()["images"]:
        if img["id"] == image_id:
            return 200, img
    return 404, {"error": {"message": f"Image not found: {image_id}"}}


def neutron_networks_doc() -> dict:
    return {
        "networks": [
            {
                "id": NETWORK1_ID,
                "name": "net-compute1",
                "status": "ACTIVE",
                "admin_state_up": True,
                "subnets": [SUBNET1_ID],
            },
            {
                "id": NETWORK2_ID,
                "name": "net-compute2",
                "status": "ACTIVE",
                "admin_state_up": True,
                "subnets": [SUBNET2_ID],
            },
        ]
    }


def neutron_subnets_doc() -> dict:
    return {
        "subnets": [
            {
                "id": SUBNET1_ID,
                "network_id": NETWORK1_ID,
                "name": "subnet-compute1",
                "cidr": "10.10.1.0/24",
                "gateway_ip": "10.10.1.1",
                "ip_version": 4,
            },
            {
                "id": SUBNET2_ID,
                "network_id": NETWORK2_ID,
                "name": "subnet-compute2",
                "cidr": "10.20.1.0/24",
                "gateway_ip": "10.20.1.1",
                "ip_version": 4,
            },
        ]
    }


def cinder_volumes_doc() -> dict:
    return {
        "volumes": [
            {
                "id": VOLUME1_ID,
                "name": "vol-compute1",
                "size": 20,
                "status": "in-use",
                "attachments": [{"server_id": SERVER_ID, "attachment_id": "att-01"}],
            },
            {
                "id": VOLUME2_ID,
                "name": "vol-compute2",
                "size": 30,
                "status": "in-use",
                "attachments": [{"server_id": SERVER2_ID, "attachment_id": "att-02"}],
            },
        ]
    }


def cinder_volume_doc(volume_id: str) -> tuple[int, dict]:
    for volume in cinder_volumes_doc()["volumes"]:
        if volume["id"] == volume_id:
            return 200, {"volume": volume}
    return 404, {"error": {"message": f"Volume not found: {volume_id}"}}


def dashboard_html() -> str:
    return """<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>OpenStack Horizon Cloud Console (2025.2 Epoxy)</title>
  <style>
    :root {
      --bg: #0b1120;
      --panel: #111827;
      --card: #1e293b;
      --border: #334155;
      --ink: #f8fafc;
      --muted: #94a3b8;
      --accent: #38bdf8;
      --brand: #e11d48;
      --ok: #10b981;
      --warn: #f59e0b;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Inter", "Pretendard", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: radial-gradient(circle at 85% 10%, rgba(56, 189, 248, 0.14), transparent 40%),
                  radial-gradient(circle at 15% 80%, rgba(225, 29, 72, 0.10), transparent 40%),
                  var(--bg);
      min-height: 100vh;
    }
    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 14px 28px;
      background: rgba(17, 24, 39, 0.92);
      border-bottom: 1px solid var(--border);
      backdrop-filter: blur(8px);
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      font-weight: 800;
      font-size: 1.15rem;
      letter-spacing: -0.02em;
    }
    .brand-logo {
      width: 32px;
      height: 32px;
      border-radius: 8px;
      background: linear-gradient(135deg, #e11d48, #f43f5e);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 900;
      color: #fff;
      box-shadow: 0 4px 12px rgba(225, 29, 72, 0.35);
    }
    .pills { display: flex; gap: 10px; align-items: center; }
    .pill {
      padding: 5px 12px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 600;
      background: rgba(56, 189, 248, 0.12);
      color: var(--accent);
      border: 1px solid rgba(56, 189, 248, 0.25);
    }
    .pill.ok {
      background: rgba(16, 185, 129, 0.14);
      color: #34d399;
      border-color: rgba(16, 185, 129, 0.3);
    }
    .wrap { max-width: 1200px; margin: 28px auto; padding: 0 24px 40px; }
    .hero {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      margin-bottom: 24px;
      gap: 16px;
      flex-wrap: wrap;
    }
    h1 { margin: 0 0 6px; font-size: 1.85rem; letter-spacing: -0.02em; }
    .meta { margin: 0; color: var(--muted); font-size: 0.95rem; }
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }
    .kpi {
      background: rgba(30, 41, 59, 0.75);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 16px 18px;
    }
    .kpi-label { font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); }
    .kpi-val { font-size: 1.65rem; font-weight: 800; margin: 6px 0 4px; color: #fff; }
    .kpi-sub { font-size: 12px; color: #34d399; }
    .grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
      margin-bottom: 24px;
    }
    .card {
      background: rgba(30, 41, 59, 0.85);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 20px;
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.25);
    }
    .card-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }
    .badge {
      display: inline-block;
      background: rgba(56, 189, 248, 0.15);
      color: var(--accent);
      border-radius: 6px;
      padding: 4px 10px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.04em;
    }
    .status-dot {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-weight: 700;
      color: #34d399;
      background: rgba(16, 185, 129, 0.12);
      padding: 4px 10px;
      border-radius: 999px;
    }
    .status-dot::before {
      content: "";
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 8px #10b981;
    }
    h2 { margin: 4px 0 14px; font-size: 1.25rem; }
    ul { margin: 0; padding: 0; list-style: none; }
    li {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 0;
      border-bottom: 1px solid rgba(51, 65, 85, 0.6);
      font-size: 0.9rem;
    }
    li:last-child { border-bottom: none; }
    .k { color: var(--muted); }
    code {
      background: rgba(15, 23, 42, 0.8);
      color: #e2e8f0;
      padding: 3px 8px;
      border-radius: 6px;
      font-family: "JetBrains Mono", "Fira Code", monospace;
      font-size: 0.82rem;
      border: 1px solid rgba(51, 65, 85, 0.8);
    }
    .topo {
      background: rgba(17, 24, 39, 0.9);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 20px;
    }
    .topo-title {
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--accent);
      margin-bottom: 12px;
      display: flex;
      justify-content: space-between;
    }
    .topo-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
    }
    .topo-box {
      background: rgba(30, 41, 59, 0.6);
      border: 1px dashed #475569;
      border-radius: 10px;
      padding: 12px;
      font-size: 0.85rem;
    }
    .topo-box strong { display: block; color: #fff; margin-bottom: 4px; }
    .topo-box span { color: var(--muted); font-size: 0.8rem; }
  </style>
</head>
<body>
  <header class="topbar">
    <div class="brand">
      <div class="brand-logo">OS</div>
      <span>OpenStack Horizon <small style="color:#94a3b8;font-weight:500;">| Private Cloud Telemetry</small></span>
    </div>
    <div class="pills">
      <span class="pill">Release: 2025.2 Epoxy</span>
      <span class="pill">Region: RegionOne</span>
      <span class="pill ok">Keystone v3.14 Stable</span>
    </div>
  </header>

  <div class="wrap">
    <div class="hero">
      <div>
        <h1>OpenStack Horizon Mock</h1>
        <p class="meta">강의 실습용 프라이빗 클라우드 대시보드: Nova Compute 2노드, Neutron OVN 격리 네트워크, Cinder NVMe 볼륨 토폴로지</p>
      </div>
      <div>
        <code>Project: admin (project-admin)</code>
      </div>
    </div>

    <div class="kpi-grid">
      <div class="kpi">
        <div class="kpi-label">Active Instances</div>
        <div class="kpi-val">2 / 2</div>
        <div class="kpi-sub">compute1 · compute2 (ACTIVE)</div>
      </div>
      <div class="kpi">
        <div class="kpi-label">vCPU &amp; Memory Pool</div>
        <div class="kpi-val">4 vCPU · 8 GB</div>
        <div class="kpi-sub">Hypervisor: KVM / Libvirt UP</div>
      </div>
      <div class="kpi">
        <div class="kpi-label">Neutron Subnets</div>
        <div class="kpi-val">2 Isolated</div>
        <div class="kpi-sub">10.10.1.0/24 · 10.20.1.0/24</div>
      </div>
      <div class="kpi">
        <div class="kpi-label">Cinder Block Storage</div>
        <div class="kpi-val">50 GB In-Use</div>
        <div class="kpi-sub">vol-compute1 (20G) · vol-compute2 (30G)</div>
      </div>
    </div>

    <div class="grid">
      <section class="card">
        <div class="card-head">
          <span class="badge">NOVA COMPUTE #1</span>
          <span class="status-dot">ACTIVE</span>
        </div>
        <h2>compute1</h2>
        <ul>
          <li><span class="k">Instance ID</span> <code>2f8cf7bb-1472</code></li>
          <li><span class="k">Flavor / Image</span> <code>m1.small · Ubuntu 24.04</code></li>
          <li><span class="k">Neutron Network</span> <code>net-compute1 (10.10.1.0/24)</code></li>
          <li><span class="k">Fixed IP</span> <code>10.10.1.11</code></li>
          <li><span class="k">Cinder Volume</span> <code>vol-compute1 (20GB)</code></li>
        </ul>
      </section>

      <section class="card">
        <div class="card-head">
          <span class="badge">NOVA COMPUTE #2</span>
          <span class="status-dot">ACTIVE</span>
        </div>
        <h2>compute2</h2>
        <ul>
          <li><span class="k">Instance ID</span> <code>7d7859f7-8f9e</code></li>
          <li><span class="k">Flavor / Image</span> <code>m1.small · Ubuntu 24.04</code></li>
          <li><span class="k">Neutron Network</span> <code>net-compute2 (10.20.1.0/24)</code></li>
          <li><span class="k">Fixed IP</span> <code>10.20.1.11</code></li>
          <li><span class="k">Cinder Volume</span> <code>vol-compute2 (30GB)</code></li>
        </ul>
      </section>

      <section class="card">
        <div class="card-head">
          <span class="badge">SERVICE CATALOG</span>
          <span class="status-dot">HEALTHY</span>
        </div>
        <h2>API Endpoints</h2>
        <ul>
          <li><span class="k">Keystone (Identity)</span> <code>/v3/auth/tokens</code></li>
          <li><span class="k">Nova (Compute)</span> <code>/v2.1/servers/detail</code></li>
          <li><span class="k">Glance (Image)</span> <code>/v2/images</code></li>
          <li><span class="k">Neutron (Network)</span> <code>/v2.0/networks</code></li>
          <li><span class="k">Cinder (Volume v3)</span> <code>/v3/project-admin/volumes</code></li>
        </ul>
      </section>
    </div>

    <div class="topo">
      <div class="topo-title">
        <span>CONTROL PLANE &amp; DATA PLANE SERVICE HEALTH</span>
        <span style="color:#34d399;">All 6 Core Daemons Reporting UP</span>
      </div>
      <div class="topo-row">
        <div class="topo-box">
          <strong>nova-scheduler</strong>
          <span>Host: controller · Zone: internal · State: UP</span>
        </div>
        <div class="topo-box">
          <strong>nova-conductor</strong>
          <span>Host: controller · Zone: internal · State: UP</span>
        </div>
        <div class="topo-box">
          <strong>nova-compute</strong>
          <span>Host: compute1 · Zone: nova · State: UP</span>
        </div>
        <div class="topo-box">
          <strong>neutron-ovn / octavia</strong>
          <span>L3 Router · LBaaS HA Ready · State: UP</span>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""


def nova_version_doc(host: str, nova_port: int) -> dict:
    base = f"http://{host}:{nova_port}/v2.1"
    return {
        "version": {
            "id": "v2.1",
            "status": "CURRENT",
            "links": [{"rel": "self", "href": base}],
        }
    }


def nova_services_doc() -> dict:
    return {
        "services": [
            {
                "id": 1,
                "binary": "nova-scheduler",
                "host": "controller",
                "zone": "internal",
                "status": "enabled",
                "state": "up",
                "updated_at": "2026-03-30T12:00:00.000000",
                "disabled_reason": None,
            },
            {
                "id": 2,
                "binary": "nova-conductor",
                "host": "controller",
                "zone": "internal",
                "status": "enabled",
                "state": "up",
                "updated_at": "2026-03-30T12:00:00.000000",
                "disabled_reason": None,
            },
            {
                "id": 3,
                "binary": "nova-compute",
                "host": "compute1",
                "zone": "nova",
                "status": "enabled",
                "state": "up",
                "updated_at": "2026-03-30T12:00:00.000000",
                "disabled_reason": None,
            },
        ]
    }


def nova_hypervisors_doc() -> dict:
    return {
        "hypervisors": [
            {
                "id": 1,
                "hypervisor_hostname": "compute1",
                "state": "up",
                "status": "enabled",
                "vcpus": 4,
                "memory_mb": 8192,
                "local_gb": 80,
                "service": {"host": "compute1", "id": 3, "disabled_reason": None},
            }
        ]
    }


class MockOpenStackHandler(BaseHTTPRequestHandler):
    host = "127.0.0.1"
    keystone_port = 5000
    nova_port = 8774

    def _send_json(self, status: int, payload: dict, headers: dict | None = None) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        if headers:
            for key, value in headers.items():
                self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, status: int, html: str) -> None:
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        return

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path in ["/healthz", "/"]:
            self._send_json(
                200,
                {
                    "status": "ok",
                    "services": {
                        "keystone": f"http://{self.host}:{self.keystone_port}/v3",
                        "nova": f"http://{self.host}:{self.keystone_port}/v2.1",
                    },
                },
            )
            return

        if self.path == "/v3":
            self._send_json(200, keystone_version_doc(self.host, self.keystone_port))
            return

        if path in ["/v2.1", "/v2.1/"]:
            self._send_json(200, nova_version_doc(self.host, self.nova_port))
            return

        if path in ["/v2.1/os-services", "/v2.1/os-services/"]:
            self._send_json(200, nova_services_doc())
            return

        if path in ["/v2.1/os-hypervisors/detail", "/v2.1/os-hypervisors/detail/", "/v2.1/os-hypervisors", "/v2.1/os-hypervisors/"]:
            self._send_json(200, nova_hypervisors_doc())
            return

        if path in ["/v2.1/servers", "/v2.1/servers/", "/v2.1/servers/detail", "/v2.1/servers/detail/"]:
            name = query.get("name", [None])[0]
            self._send_json(200, nova_servers_doc(name=name))
            return

        if path.startswith("/v2.1/servers/"):
            server_id = path.strip("/").split("/")[-1]
            for server in nova_servers_doc()["servers"]:
                if server_id == server["id"]:
                    self._send_json(200, {"server": server})
                    return
            self._send_json(404, {"error": {"message": f"Server not found: {server_id}"}})
            return

        if path in ["/v2.0/networks", "/v2.0/networks/"]:
            self._send_json(200, neutron_networks_doc())
            return

        if path in ["/v2.0/subnets", "/v2.0/subnets/"]:
            self._send_json(200, neutron_subnets_doc())
            return

        if path in ["/v2", "/v2/"]:
            self._send_json(200, glance_versions_doc(self.host, self.keystone_port))
            return

        if path in ["/v2/images", "/v2/images/"]:
            self._send_json(200, glance_images_doc())
            return

        if path.startswith("/v2/images/"):
            image_id = path.strip("/").split("/")[-1]
            status, payload = glance_image_doc(image_id)
            self._send_json(status, payload)
            return

        if path in ["/v3/project-admin/volumes", "/v3/project-admin/volumes/", "/v3/project-admin/volumes/detail", "/v3/project-admin/volumes/detail/"]:
            self._send_json(200, cinder_volumes_doc())
            return

        if path.startswith("/v3/project-admin/volumes/"):
            volume_id = path.strip("/").split("/")[-1]
            status, payload = cinder_volume_doc(volume_id)
            self._send_json(status, payload)
            return

        if path == "/dashboard":
            self._send_html(200, dashboard_html())
            return

        self._send_json(404, {"error": {"message": f"Path not found: {self.path}"}})

    def do_POST(self) -> None:
        if self.path == "/v3/auth/tokens":
            self._send_json(
                201,
                token_doc(self.host, self.keystone_port, self.nova_port),
                headers={"X-Subject-Token": TOKEN_ID},
            )
            return

        self._send_json(404, {"error": {"message": f"Path not found: {self.path}"}})


class ReusableThreadingHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--keystone-port", type=int, default=5000)
    parser.add_argument("--nova-port", type=int, default=8774)
    args = parser.parse_args()

    MockOpenStackHandler.host = args.host
    MockOpenStackHandler.keystone_port = args.keystone_port
    MockOpenStackHandler.nova_port = args.nova_port

    server = ReusableThreadingHTTPServer((args.host, args.keystone_port), MockOpenStackHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
