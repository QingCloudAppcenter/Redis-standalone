#! /bin/bash
#
# Copyright (C) 2015 Yunify Inc.
#
# Script to stop redis-server.

PID=$(pidof redis-server)
if [ -z "$PID" ]; then
    echo "redis-server is not running" > /var/log/redis.log 2>&1
    exit 0
fi

# Try to terminate redis-server
kill -SIGTERM $PID

# Check if redis-server is terminated
for i in $(seq 0 2); do
   if ! ps -ef | grep ^stop-redis-server > /dev/null; then
       echo "redis-server is successfully terminated" >> /var/log/redis.log 2>&1
       exit 0
   fi
   sleep 1
done

# Not terminated yet, now I am being rude!
# In case of a new redis-server process is somebody else (unlikely though),
# we get the pid again here.
kill -9 $(pidof redis-server)
if [ $? -eq 0 ]; then
    echo "redis-server is successfully killed" >> /var/log/redis.log 2>&1
    exit 0
else
    echo "Failed to kill redis-server" >> /var/log/redis.log 2>&1
    exit 1
fi
