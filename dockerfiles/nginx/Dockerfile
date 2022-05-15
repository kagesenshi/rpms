FROM quay.io/centos/centos:stream9

RUN dnf update -y && \
    dnf install iputils net-tools nmap bind-utils glibc-langpack-en -y && \
    dnf clean all 

RUN dnf install nginx -y && \
    dnf clean all

USER root

ENV LC_ALL=en_US.utf8 \
    LANG=en_US.utf8

EXPOSE 80/tcp 443/tcp
ENTRYPOINT ["/usr/sbin/nginx"]
