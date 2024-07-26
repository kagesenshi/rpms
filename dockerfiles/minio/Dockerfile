FROM registry.gitlab.com/abyres/releases/centos8:8-1 AS base

ENV MINIO_RELEASE=20221126224332.0.0

RUN dnf install https://dl.min.io/server/minio/release/linux-amd64/minio-${MINIO_RELEASE}.x86_64.rpm -y && \
    dnf clean all && \
    groupadd -r minio-user && \
    useradd -r -g minio-user -d /data -s /sbin/nologin minio-user

USER minio-user

ENV LC_ALL=en_US.utf8 \
    LANG=en_US.utf8

EXPOSE 9000/tcp 9001/tcp

ENTRYPOINT ["/usr/local/bin/minio", "server", "--console-address", ":9001"]

FROM base AS client

ENTRYPOINT ["/usr/local/bin/mc"]
