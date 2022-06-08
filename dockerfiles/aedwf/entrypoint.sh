#!/bin/bash

export AIRFLOW_HOME="/etc/apache-airflow"
export PATH="/opt/apache-airflow/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

if [ "$1" == "start" ];then
    /opt/apache-airflow/bin/airflow webserver --pid /tmp/airflow.pid
elif [ "$1" == "worker" ];then
    /opt/apache-airflow/bin/airflow celery worker --pid /tmp/airflow-worker.pid
elif [ "$1" == "scheduler" ];then
    /opt/apache-airflow/bin/airflow scheduler --pid /tmp/airflow-scheduler.pid
elif [ "$1" == "first-init" ];then
    /opt/apache-airflow/bin/airflow db upgrade
    /opt/apache-airflow/bin/airflow users create --username admin --firstname admin --lastname user --email admin@localhost.local --password admin --role Admin
else
    /usr/bin/apache-airflow "$@"
fi
