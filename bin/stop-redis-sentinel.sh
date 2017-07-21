#! /bin/bash
#
# Copyright (C) 2015 Yunify Inc.
#
# Script to stop redis-sentinel.

PID=$(pidof redis-sentinel)
if [ -z "$PID" ]; then
    echo "redis-sentinel is not running" > /var/log/sentinel.log 2>&1
    exit 0
fi

# Try to terminate redis-sentinel
kill -SIGTERM $PID

# Check if redis-sentinel is terminated
for i in $(seq 0 2); do
   if ! ps -ef | grep ^stop-redis-sentinel > /dev/null; then
       echo "redis-sentinel is successfully terminated" >> /var/log/sentinel.log 2>&1
       exit 0
   fi
   sleep 1
done

# In case of a new redis-sentinel process is somebody else (unlikely though),
# we get the pid again here.
kill -9 $(pidof redis-sentinel)
if [ $? -eq 0 ]; then
    echo "redis-sentinel is successfully killed" >> /var/log/sentinel.log 2>&1
    exit 0
else
    echo "Failed to kill redis-sentinel" >> /var/log/sentinel.log 2>&1
    exit 1
fi
