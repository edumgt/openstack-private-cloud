SHELL := /bin/bash

.PHONY: help bootstrap lint test web mock-api inventory-aws molecule

help:
	@echo "=================================================================="
	@echo "  OpenStack Private Cloud & Ansible IaC Automation Lab (v2.0)"
	@echo "=================================================================="
	@echo "  make bootstrap     - Install Ansible Core, Galaxy collections & Python deps"
	@echo "  make lint          - Run ansible-lint & ruff Python linter"
	@echo "  make test          - Run pytest suite (RAG, Mock OpenStack, Web API)"
	@echo "  make web           - Launch FastAPI Web Control Center on :8000"
	@echo "  make mock-api      - Launch Mock OpenStack Keystone/Nova/Horizon on :5000"
	@echo "  make inventory-aws - Render AWS EC2 Dynamic Inventory graph"
	@echo "  make molecule      - Run Molecule role verification tests"

bootstrap:
	./scripts/bootstrap.sh

lint:
	ansible-lint
	ruff check lab/ web_tester/ scripts/mock_openstack_api.py

test:
	pytest -v

web:
	uvicorn web_tester.app:app --host 0.0.0.0 --port 8000 --reload

mock-api:
	python3 scripts/mock_openstack_api.py --host 0.0.0.0 --keystone-port 5000 --nova-port 8774

inventory-aws:
	ansible-inventory -i ansible/inventories/aws/aws_ec2.yml --graph

molecule:
	molecule test
