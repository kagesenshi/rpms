#!/bin/bash

BINDIR='/opt/apache/spark3/bin/'

$BINDIR/$1 "${@:2}"
