FROM registry.gitlab.com/abyres/releases/centos8:latest

RUN /usr/sbin/groupadd -r postgres --gid 1000 && \
     /usr/sbin/useradd -r -g postgres --uid 1000 \
     -s /sbin/nologin postgres

RUN set -ex && \
    dnf install https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm -y && \
    wget 'https://repos.citusdata.com/community/config_file.repo?os=RHEL&dist=8&source=script' -O /etc/yum.repos.d/citus_community.repo && \
    dnf config-manager --set-disabled pgdg\* && \
    dnf config-manager --set-enabled pgdg14 && \
    dnf module disable postgresql -y && \
    dnf install -y citus102_14 && \
    dnf clean all

WORKDIR /var/lib/pgsql/
ENV PGDATA=/var/lib/pgsql/
ADD entrypoint.sh /opt/entrypoint.sh
ADD createdb_with_user.sh /usr/bin/
ADD pg_hba.conf /etc/pg_hba.conf
RUN chown postgres:postgres /etc/pg_hba.conf && \
    chmod a+rx /usr/bin/createdb_with_user.sh && \
    chmod +x /opt/entrypoint.sh
USER postgres

ENTRYPOINT [ "/opt/entrypoint.sh" ]
