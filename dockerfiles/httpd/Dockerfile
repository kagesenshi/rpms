FROM registry.gitlab.com/abyres/releases/centos8:8-1

RUN /usr/sbin/groupadd -r apache --gid 1000 && \
     /usr/sbin/useradd -r -g apache --uid 1000 \
     -s /sbin/nologin apache

RUN dnf install httpd -y && \
    dnf clean all

EXPOSE 80
EXPOSE 443

VOLUME /var/www/html

CMD ["/usr/bin/httpd","-f","FOREGROUND"]
