#!/bin/bash

MASTER_IP=$6
LOCAL_IP=`curl http://metadata/self/host/ip`
VIP=`curl http://metadata/self/cluster/endpoints/reserved_ips/vip/value`
NETMASK='24'
INTERFACE='eth0'


if [ "x${MASTER_IP}" = "x${LOCAL_IP}" ]; then
    /sbin/ip addr add ${VIP}/${NETMASK} dev ${INTERFACE}
    /sbin/arping -q -c 3 -A ${VIP} -I ${INTERFACE}
    exit 0
else
    /sbin/ip addr del ${VIP}/${NETMASK} dev ${INTERFACE}
    exit 0
fi

exit 1
