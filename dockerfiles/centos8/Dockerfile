FROM centos:stream8

ADD dnf.conf /etc/dnf/dnf.conf

RUN dnf install dnf-plugins-core epel-release -y && \
    dnf install -y bash iputils glibc-langpack-en net-tools \
        nmap bind-utils hostname tini nss pam wget && \
    dnf clean all
