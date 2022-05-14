FROM quay.io/centos/centos:stream9

RUN dnf update -y && \
    dnf clean all 

RUN dnf install glibc-langpack-en redis -y && \
    dnf clean all

USER redis

ENV LC_ALL=en_US.utf8 \
    LANG=en_US.utf8

EXPOSE 6379/tcp
ENTRYPOINT ["/usr/bin/redis-server", "/etc/redis/redis.conf", "--daemonize","no"]
