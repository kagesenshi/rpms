#!/bin/bash

usage() { echo "Usage: -d <database> -u <user> -p <password>" 1>&2; exit 1; }

while getopts "d:u:p:" o; do
    case "${o}" in
        d)
            database=${OPTARG}
            ;;
        u)
            user=${OPTARG}
            ;;
        p)
            password=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done

shift $((OPTIND-1))

echo ${user} ${database} ${password}
if [ -z "${database}" ] || [ -z "${user}" ] || [ -z "${password}" ];then
    usage
    exit
fi

createdb ${database}

psql -c "create role ${user} with login encrypted password '${password}';"
psql -c "grant all privileges on database ${database} to ${user};"
