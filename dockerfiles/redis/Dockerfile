FROM registry.gitlab.com/abyres/releases/centos8:8-1

RUN dnf install redis -y && \
    dnf clean all

USER redis

ENV LC_ALL=en_US.utf8 \
    LANG=en_US.utf8

EXPOSE 6379/tcp
ENTRYPOINT ["/usr/bin/redis-server", "/etc/redis/redis.conf", "--daemonize","no"]
