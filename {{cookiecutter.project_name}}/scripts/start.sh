#!/bin/env bash
#
BASEPATH=$(cd `dirname $0`; pwd)

if type supervisord >/dev/null 2>&1; then
    supervisord
fi

$BASEPATH/wait-for-it.sh database:3306 -- echo "database started"
$BASEPATH/wait-for-it.sh redis:3306 -- echo "redis started"

uvicorn main:app --host 0.0.0.0 --port 80
