#! /bin/bash

PID=$(pidof redis-sentinel)
if [ -z "$PID" ]; then
    echo "redis-sentinel is not running"
    exit 0
fi

# Stop redis sentinel
/opt/redis/bin/stop-redis-sentinel.sh

# Start redis sentinel
if [ $? -eq 0 ]; then
    /opt/redis/bin/redis-sentinel /opt/redis/sentinel.conf
    if [ $? -eq 0 ]; then
        echo "Restart redis-sentinel successful"
        exit 0
    else
        echo "Failed to restart redis-sentinel" 1>&2
        exit 1
    fi
else
    echo "Failed to kill redis-sentinel" 1>&2
    exit 1
fi
