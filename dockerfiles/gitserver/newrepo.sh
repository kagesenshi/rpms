#!/bin/bash

cd /srv/git
if [ ! -d "$1.git" ];then
    git init --bare $1.git
    cd /tmp/
    git clone /srv/git/$1.git $1.repo
    cd $1.repo/
    echo "$1" > README.txt
    git add README.txt
    git -c user.name="git" -c user.email="git@`hostname`" commit -m "Initial commit"
    git push origin master
    cd /srv/git
    rm -rf /tmp/$1.repo
    chown -R git:git /srv/git/$1.git
else
    echo "Repo $1 already exists"
fi
