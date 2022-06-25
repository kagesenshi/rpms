#!/bin/bash

if [ "$1" == "schematool" ];then
    /opt/apache/hive/bin/hive --service schemaTool -dbType ${DB_TYPE} -validate
    if [ "x$?"  != "x0" ];then
        /opt/apache/hive/bin/hive --service schemaTool -dbType ${DB_TYPE} "${@:2}"
    fi
elif [ "$1" == "metastore" ];then
    /opt/apache/hive/bin/hive --service metastore "${@:2}"
elif [ "$1" == "noop" ];then
    tail -f /dev/null
else
    /opt/apache/hive/bin/$1 "${@:2}"
fi
