#!/bin/bash
set -e

BINDIR="/usr/pgsql-14/bin"
SHAREDIR="/usr/pgsql-14/share"

if [ "$1" == "start" ];then
    $BINDIR/postgresql-14-check-db-dir ${PGDATA}
    cp /etc/pg_hba.conf ${PGDATA}/pg_hba.conf
    chmod og-rwx ${PGDATA}/pg_hba.conf
    sed -i 's|logging_collector = on|logging_collector = off|g' ${PGDATA}/postgresql.conf
    $BINDIR/postmaster -D ${PGDATA} -h 0.0.0.0 "${@:2}"
elif [ "$1" == "initdb" ];then
    if [ ! -f "${PGDATA}/PG_VERSION" ];then
        $BINDIR/initdb --pgdata=${PGDATA} -A md5 --auth-local=peer --encoding=UTF8 --pwfile $SHAREDIR/postgresql.conf.sample 
    fi
else
    "$@"
fi
