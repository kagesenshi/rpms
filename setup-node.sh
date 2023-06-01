#!/bin/bash


PARSED=$(getopt -a -n setup-node -o :n:i: --long name:,ip: -- "$@")
VALID_ARGS=$?

usage() {
   echo "Usage: $0 -n [NAME] -i [IP]"
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

set -x

nmcli con mod enp1s0 ipv4.addresses ${IP}/24
nmcli con mod enp1s0 ipv4.gateway ${GATEWAY}
nmcli con mod enp1s0 ipv4.dns ${DNS}
nmcli con mod enp1s0 ipv4.method manual

cat << EOF > /etc/NetworkManager/conf.d/99-dns-none.conf
[main]
dns=none
EOF

cat << EOF > /etc/resolv.conf
nameserver ${DNS}
EOF

echo ${NAME}.${IP}.sslip.io > /etc/hostname
nmcli con up enp1s0
hostname `cat /etc/hostname`
