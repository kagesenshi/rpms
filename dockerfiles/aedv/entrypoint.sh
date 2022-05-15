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
else
    /usr/bin/apache-superset "$@"
fi
