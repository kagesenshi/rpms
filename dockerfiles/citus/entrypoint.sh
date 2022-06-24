#!/bin/bash
set -e

BINDIR="/usr/pgsql-14/bin"
SHAREDIR="/usr/pgsql-14/share"

if [ "$1" == "start" ];then
    $BINDIR/postgresql-14-check-db-dir ${PGDATA}
    $BINDIR/postmaster -D ${PGDATA} -h 0.0.0.0 "${@:2}"
elif [ "$1" == "initdb" ];then
    $BINDIR/initdb --pgdata=${PGDATA} -A scram-sha-256 --auth-local=peer --pwfile $SHAREDIR/postgresql.conf.sample 
else
    "$@"
fi
