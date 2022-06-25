#!/bin/bash

REPO="registry.gitlab.com/abyres/releases/gitserver"
TAG="latest"

docker build -t $REPO:$TAG .

if [ "$1" == "push" ];then
   docker push $REPO:$TAG
fi
