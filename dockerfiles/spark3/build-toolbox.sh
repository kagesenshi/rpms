#!/bin/bash -x

set -e

REPO="registry.gitlab.com/abyres/releases/spark3-toolbox"
TAG="latest"

docker build -t $REPO:$TAG -f Toolbox .

if [ "$1" == "push" ];then
   docker push $REPO:$TAG
fi  

