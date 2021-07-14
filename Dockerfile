FROM alpine:3.12
 
ENV ANSIBLE_VERSION 2.9.10
 
ENV BUILD_PACKAGES \
  bash \
  curl \
  tar \
  openssh-client \
  sshpass \
  git \
  python3 \
  py3-boto \
  py3-dateutil \
  py3-httplib2 \
  py3-jinja2 \
  py3-paramiko \
  py3-pip \
  py3-yaml \
  ca-certificates  

RUN set -x && \
    \
    echo "==> Adding build-dependencies..."  && \
    apk --update add --virtual build-dependencies \
      gcc \
      musl-dev \
      libffi-dev \
      openssl-dev \
      python3-dev && \
    \
    echo "==> Upgrading apk and system..."  && \
    apk update && apk upgrade && \
    \
    echo "==> Adding Python runtime..."  && \
    apk add --no-cache ${BUILD_PACKAGES} && \
    pip3 install --upgrade pip && \
    pip3 install python-keyczar docker-py pywinrm requests ansible-tower-cli omsdk && \
    \
    echo "==> Installing Ansible..."  && \
    pip3 install ansible==${ANSIBLE_VERSION} && \
    \
    echo "==> Cleaning up..."  && \
    apk del build-dependencies && \
    rm -rf /var/cache/apk/* && \
    \
    echo "==> Adding hosts for convenience..."  && \
    mkdir -p /etc/ansible /etc/tower /ansible/collections /ansible/files /usr/share/ansible/plugins && \
    echo "[local]" >> /etc/ansible/hosts && \
    echo "localhost" >> /etc/ansible/hosts 
 
COPY ansible.cfg /etc/ansible/ansible.cfg
RUN chmod 444 /etc/ansible/ansible.cfg

COPY tower_cli.cfg /etc/tower/tower_cli.cfg
RUN chmod 444 /etc/tower/tower_cli.cfg

COPY collections/requirements.yml /ansible/collections/requirements.yml
RUN ansible-galaxy collection install -r /ansible/collections/requirements.yml

ENV PYTHONPATH /ansible/lib
ENV PATH /ansible/bin:$PATH
 
WORKDIR /ansible
 
CMD ansible-playbook --version