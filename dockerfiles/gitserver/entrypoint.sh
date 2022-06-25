#!/bin/bash

HOMEDIR=/home/git/
mkdir -p ${HOMEDIR}/.ssh/

if [ "x${GIT_SSH_PUBKEYS}" != "x" ];then
    while IFS=';' read -ra KEY; do
    for i in "${KEY[@]}"; do
        echo $i >> ${HOMEDIR}/.ssh/authorized_keys
    done
    done <<< "${GIT_SSH_PUBKEYS}"
fi

chown git:git -R ${HOMEDIR}/
chmod og-rwx -R ${HOMEDIR}/.ssh/

if [ "$1" == "sshd" ];then
    /usr/libexec/openssh/sshd-keygen rsa
    /usr/libexec/openssh/sshd-keygen ecdsa
    /usr/libexec/openssh/sshd-keygen ed25519

    /usr/sbin/sshd -D
elif [ "$1" == "gitweb" ];then
    cat << EOF > /etc/gitweb.conf
our \$projectroot = "/srv/git/";
our @git_base_url_list = ("$INGRESS_HOST");
EOF
    touch /etc/htpasswd
    htpasswd -b /etc/htpasswd "${GITWEB_USER}" "${GITWEB_PASSWORD}"
    /usr/sbin/httpd -c "User git" -D FOREGROUND
else
    echo "Unknown command"
fi
