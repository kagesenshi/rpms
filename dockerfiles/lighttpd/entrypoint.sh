#!/bin/bash

if [ "$1" == "start" ];then
  if [ "$LIGHTTPD_CONFIGx" == "x" ];then
    >&2 echo '$LIGHTTPD_CONFIG environment is not set'
  fi
  lighttpd -D -f "$LIGHTTPD_CONFIG"
else
  "$@"
fi
