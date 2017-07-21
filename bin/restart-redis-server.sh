#! /bin/bash

PID=$(pidof redis-server)
if [ -z "$PID" ]; then
    echo "redis-server is not running"
    exit 0
fi

# Stop redis server
/opt/redis/bin/stop-redis-server.sh

# Start redis server
if [ $? -eq 0 ]; then
    /opt/redis/bin/redis-server /opt/redis/redis.conf
    if [ $? -eq 0 ]; then
        echo "Restart redis-server successful"
        exit 0
    else
        echo "Failed to restart redis-server" 1>&2
        exit 1
    fi
else
    echo "Failed to kill redis-server" 1>&2
    exit 1
fi
