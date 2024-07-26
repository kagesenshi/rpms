FROM registry.access.redhat.com/ubi8/ubi:latest

RUN dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm -y && \
    /usr/bin/crb enable && \
    dnf install python3-requests python3-pyyaml procps-ng iputils iproute bind-utils lighttpd tini -y && \
    dnf clean all && \
    curl https://dl.k8s.io/release/v1.30.0/bin/linux/amd64/kubectl -o /usr/bin/kubectl && \
    chmod +x /usr/bin/kubectl

ADD entrypoint.sh /opt/
RUN chmod a+x /opt/entrypoint.sh

ENTRYPOINT ["tini", "/opt/entrypoint.sh"]
