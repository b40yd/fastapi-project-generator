#!/bin/env bash
#

wait_for () {
    while :
    do
        (echo > /dev/tcp/mysql/3306) >/dev/null 2>&1

        if [[ $? -eq 0 ]];then
            #alembic revision --autogenerate -m "init web service databases."
            #alembic upgrade head
            uvicorn app.main:app --host 0.0.0.0 --port 80
            break
        fi

        sleep 1
    done
}


if type supervisord >/dev/null 2>&1; then
    supervisord
fi

wait_for

exit $?
