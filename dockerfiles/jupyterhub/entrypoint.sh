#!/bin/bash
set -e

TOKEN=${JUPYTER_LAB_TOKEN-''}

if [ "$1" == "debug" ];then
    tail -f /dev/null
elif [ "$1" == "hub" ];then
    jupyterhub
elif [ "$1" == "lab" ];then
    /opt/jupyterhub/bin/jupyter lab --ip 0.0.0.0 --port 8000 --NotebookApp.token="${TOKEN}"
fi
