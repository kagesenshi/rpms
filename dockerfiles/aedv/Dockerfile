FROM registry.gitlab.com/abyres/releases/fedora:35-1

LABEL org.opencontainers.image.version=1.4.2-1

RUN dnf update -y && \
    dnf copr enable izhar/data-engineering -y && \
    dnf copr enable izhar/aet -y && \
    dnf install mariadb-connector-c apache-superset -y && \
    dnf swap apache-superset-logos aedv-logos -y && \
    dnf clean all

RUN dnf install chromium -y && \
    dnf clean all 

ADD entrypoint.sh /usr/bin/entrypoint.sh
RUN chmod a+x /usr/bin/entrypoint.sh
WORKDIR /var/lib/apache-superset/
USER apache-superset

ENV PYTHONPATH=/etc/apache-superset \
    ACCESS_LOG=/var/log/apache-superset/access.log \
    ERROR_LOG=/var/log/apache-superset/errors.log \
    PYTHONUNBUFFERED=1 \
    LC_ALL=en_US.utf8 \
    LANG=en_US.utf8

ENTRYPOINT ["/usr/bin/entrypoint.sh"]
