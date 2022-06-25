#!/bin/bash

set -e

REPO="registry.gitlab.com/abyres/releases/spark3"
TOOLBOX_REPO="registry.gitlab.com/abyres/releases/spark3-toolbox"
TAG="latest"

docker build -t $REPO:$TAG .

if [ "$1" == "push" ];then
   docker push $REPO:$TAG
fi  

docker build -t $TOOLBOX_REPO:$TAG . -f Toolbox

if [ "$1" == "push" ];then
   docker push $TOOLBOX_REPO:$TAG
fi  

