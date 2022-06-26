#!/bin/bash

REPO="registry.gitlab.com/abyres/releases/centos8"

while getopts "t:p" arg; do
  case $arg in
    t)
      TAG=$OPTARG
      ;;
    p)
      PUSH="yes"
      ;;
  esac
done

TAG="${TAG:-latest}"

set -e 

docker build -t $REPO:$TAG .

if [ "$PUSH" == "yes" ];then
   docker push $REPO:$TAG
fi
