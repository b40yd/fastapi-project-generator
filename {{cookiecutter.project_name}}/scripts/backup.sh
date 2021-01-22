#！/bin/bash

BASEPATH=$(cd `dirname $0`; pwd)
BACKUPS=${BACKUPS:-"backups"}
DATABASES=${DATABASES:-"--all-databases"}
PORT=${PORT:3306}

echoerr() { if [[ $QUIET -ne 1 ]]; then echo "$@" 1>&2; fi }

usage()
{
    cat << USAGE >&2
Usage:
    $cmdname host:port [-s] [-t timeout] [-- command args]
    -h HOST | --host=HOST       Host or IP under test
    -p PORT | --port=PORT       TCP port under test
                                Alternatively, you specify the host and port as host:port
    -u USER | --user=USERNAME   database username
    -- COMMAND ARGS             Execute command with args after the test finishes
USAGE
    exit 1
}


while [[ $# -gt 0 ]]
do
    case "$1" in
        *:* )
            hostport=(${1//:/ })
            HOST=${hostport[0]}
            PORT=${hostport[1]}
            shift 1
            ;;
        -h)
            HOST="$2"
            if [[ $HOST == "" ]]; then break; fi
            shift 2
            ;;
        --host=*)
            HOST="${1#*=}"
            shift 1
            ;;
        -p)
            PORT="$2"
            if [[ $PORT == "" ]]; then break; fi
            shift 2
            ;;
        --port=*)
            PORT="${1#*=}"
            shift 1
            ;;
        -u)
            USER="$2"
            if [[ $USER == "" ]]; then break; fi
            shift 2
            ;;
        --user=*)
            USER="${1#*=}"
            shift 1
            ;;
        -P)
            PASSWD="$2"
            if [[ $PASSWD == "" ]]; then break; fi
            shift 2
            ;;
        --passwd=*)
            PASSWD="${1#*=}"
            shift 1
            ;;
        -d)
            DATABASES="$2"
            if [[ $DATABASES == "" ]]; then break; fi
            shift 2
            ;;
        --databases=*)
            DATABASES="${1#*=}"
            shift 1
            ;;
        -d)
            TABLES="$2"
            if [[ $TABLES == "" ]]; then break; fi
            shift 2
            ;;
        --tables=*)
            TABLES="${1#*=}"
            shift 1
            ;;
        --)
            shift
            FORIT_CLI=("$@")
            break
            ;;
        -H)
            usage
            ;;
        --help)
            usage
            ;;
        *)
            echoerr "Unknown argument: $1"
            usage
            ;;
    esac
done

if [[ "$HOST" == "" || "$PORT" == "" ]]; then
    echoerr "Error: you need to provide a host and port backup."
    usage
fi
if [ ! -d $BASEPATH/$BACKUPS ]; then
	mkdir -pv $BASEPATH/$BACKUPS
fi

if [[ "$USER" != "" && "$PASSWD" != "" ]]; then
    # echo "mysqldump -h $HOST -P$PORT  -u root -p $DATABASES $TABLES > $BACKUPS/$(date +'%Y-%m-%d_%H_%M_%S').sql"
    mysqldump -h $HOST -P $PORT -u $USER -p${PASSWD} $DATABASES $TABLES > $BASEPATH/$BACKUPS/$(date +'%Y-%m-%d_%H_%M_%S').sql
    if [ $? -ne 0 ];then
        echoerr "Error: $HOST:$PORT $DATABASES backup failed."
        exit 1
    fi
else
    echoerr "Error: user and passwd must not empty."
    exit 1
fi
if [[ $FORIT_CLI != "" ]]; then
    exec "${FORIT_CLI[@]}"
fi

exit 0
