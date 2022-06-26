FROM registry.gitlab.com/abyres/releases/centos8:8-1

RUN dnf install git git-lfs git-subtree git-instaweb openssh-server gitweb -y && \
    dnf clean all

RUN /usr/sbin/groupadd -r git --gid 1000 && \
     /usr/sbin/useradd -r -g git --uid 1000 \
     -m -d /home/git \
     -s /bin/bash git

ADD git-http.conf /etc/httpd/conf.d/git-http.conf
ADD entrypoint.sh /opt/entrypoint.sh
ADD newrepo.sh /usr/local/bin/newrepo
ADD gitweb.conf /etc/gitweb.conf

RUN chmod a+rx /opt/entrypoint.sh && \
    chmod a+rx /usr/local/bin/newrepo && \
    mkdir /srv/git && \
    chown -R git:git /srv/git

EXPOSE 22
EXPOSE 80
VOLUME /srv/git/

ENTRYPOINT ["/opt/entrypoint.sh"]
