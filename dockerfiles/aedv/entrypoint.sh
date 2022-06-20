#!/bin/bash

if [ "$1" == "start" ];then
    /opt/apache-superset/bin/gunicorn \
        -b 0.0.0.0:8999 \
        -w 4 \
        -k gevent \
        --timeout 120 \
        --limit-request-line 0 \
        --limit-request-field_size 0 \
        --forwarded-allow-ips="*" \
        "superset.app:create_app()"
elif [ "$1" == "worker" ];then
    /opt/apache-superset/bin/celery worker \
        --app=superset.tasks.celery_app:app --pool=prefork -O fair -c ${CELERY_WORKERS:-4}
elif [ "$1" == "scheduler" ];then
    /opt/apache-superset/bin/celery beat --app=superset.tasks.celery_app:app
elif [ "$1" == "first-init" ];then
    /usr/bin/apache-superset db upgrade
    /usr/bin/apache-superset fab create-admin --username admin --firstname admin --lastname user --email admin@localhost.local --password admin
    /usr/bin/apache-superset init
else
    /usr/bin/apache-superset "${@:2}"
fi
