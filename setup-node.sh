#!/bin/bash


PARSED=$(getopt -a -n setup-node -o :n:i:g:d:c: --long name:,ip:,gateway:,dns:,connection: -- "$@")
VALID_ARGS=$?

usage() {
   echo "Usage: $0 -n [NAME] -i [IP] -g [GATEWAY] -d [DNS] -c [NMCONN]"
   exit 1
}

if [ "$VALID_ARGS" != "0" ];then
  usage
fi

eval set -- "$PARSED"
while :
do 
  case "$1" in
     -n | --name) NAME="$2"; shift 2 ;;
     -i | --ip) IP="$2"; shift 2 ;;
     -g | --gateway) GATEWAY="$2"; shift 2;;
     -d | --dns) DNS="$2"; shift 2;;
     -c | --connection) CONN="$2"; shift 2;;
     --) shift; break;;
     *) echo "Invalid option $1"; usage;;

  esac
done

if [ "x$NAME" == "x" ];then 
   usage
fi

if [ "x$IP" == "x" ];then
   usage
fi

if [ "x$GATEWAY" == "x" ];then
   usage
fi

if [ "x$DNS" == "x" ];then
   usage
fi

if [ "x$CONN" == "x" ];then
   usage
fi

set -x

nmcli con mod "${CONN}" ipv4.addresses ${IP}/24
nmcli con mod "${CONN}" ipv4.gateway ${GATEWAY}
nmcli con mod "${CONN}" ipv4.dns ${DNS}
nmcli con mod "${CONN}" ipv4.method manual

cat << EOF > /etc/NetworkManager/conf.d/99-dns-none.conf
[main]
dns=none
EOF

cat << EOF > /etc/resolv.conf
nameserver ${DNS}
EOF

echo ${NAME}.${IP}.sslip.io > /etc/hostname
nmcli con up "${CONN}"
hostname `cat /etc/hostname`
