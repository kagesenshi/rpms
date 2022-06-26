FROM fedora:35

ADD dnf.conf /etc/dnf/dnf.conf

RUN dnf install dnf-plugins-core -y && \
    dnf install -y bash iputils glibc-langpack-en net-tools \
        nmap bind-utils hostname tini nss pam wget \
        procps-ng vim-enhanced && \
    dnf clean all

RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

ENV LC_ALL=en_US.utf8 \
    LANG=en_US.utf8
