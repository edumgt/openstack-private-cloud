FROM python:3.13-slim

LABEL org.opencontainers.image.title="OpenStack Private Cloud & Ansible Lab" \
      org.opencontainers.image.description="Enterprise Private Cloud (OpenStack 2025.2 Epoxy) & Ansible IaC Hands-on Lab" \
      org.opencontainers.image.source="https://github.com/edumgt/openstack-private-cloud"

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ANSIBLE_HOST_KEY_CHECKING=False \
    ANSIBLE_RETRY_FILES_ENABLED=False

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    jq \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.yml pyproject.toml ./

RUN python -m pip install --upgrade pip \
    && python -m pip install "ansible-core>=2.17" \
    && if [ -f requirements.txt ]; then python -m pip install -r requirements.txt; fi \
    && if [ -f requirements.yml ]; then ansible-galaxy collection install -r requirements.yml; fi

COPY . .

EXPOSE 8000 5000 8774

CMD ["bash"]
