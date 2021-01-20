#!/bin/env bash
#

if type supervisord >/dev/null 2>&1; then
    supervisord
fi

./wait-for-it.sh database:3306 -- echo "database started"
./wait-for-it.sh redis:3306 -- echo "redis started"

uvicorn app.main:app --host 0.0.0.0 --port 80

