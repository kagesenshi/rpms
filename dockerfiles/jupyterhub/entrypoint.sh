#!/bin/bash
set -e

TOKEN=${JUPYTER_LAB_TOKEN-''}

if [ "$1" == "debug" ];then
    tail -f /dev/null
elif [ "$1" == "hub" ];then
    jupyterhub -f /etc/jupyterhub/jupyterhub_config.py
elif [ "$1" == "lab" ];then
    /opt/jupyterhub/bin/jupyter lab --ip 0.0.0.0 --port 8000 --NotebookApp.token="${TOKEN}"
elif [ "$1" == "jupyterhub-singleuser" ];then
    export K8S_POD_NAME=`hostname -s`
    userdel -f jupyter
    groupadd ${JUPYTERHUB_USER} -g 1000
    useradd ${JUPYTERHUB_USER} -u 1000 -g 1000
    cd /home/${JUPYTERHUB_USER}
    sudo -E -u ${JUPYTERHUB_USER} -- env "PATH=$PATH" "$@"
else
    "$@"
fi
