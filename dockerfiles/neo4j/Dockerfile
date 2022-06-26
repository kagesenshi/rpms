FROM centos:stream8

RUN dnf update -y && \
    dnf install iputils net-tools nmap bind-utils glibc-langpack-en -y && \
    dnf clean all 

ADD neo4j.repo /etc/yum.repos.d/

RUN dnf install neo4j -y && \
    dnf clean all

RUN /usr/sbin/groupadd -r neouser --gid 1000 && \
     /usr/sbin/useradd -r -g neouser --uid 1000 \
     -s /sbin/nologin neouser

ADD entrypoint.sh /opt/
RUN chmod a+x /opt/entrypoint.sh && \
    chown neouser:neouser -R /var/lib/neo4j/ /var/log/neo4j/

USER neouser

ENV LC_ALL=en_US.utf8 \
    LANG=en_US.utf8 \
    NEO4J_CONF=/etc/neo4j \
    NEO4J_HOME=/var/lib/neo4j

ENTRYPOINT ["/opt/entrypoint.sh"]
