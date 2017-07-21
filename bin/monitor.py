#!/usr/bin/python

import redis
import os
import sys
import json
import Constants

REDIS_STATIC_KEYS = ['used_memory',
                     'total_connections_received',
                     'connected_clients',
                     'expired_keys',
                     'evicted_keys',
                     'keyspace_hits',
                     'keyspace_misses',
                     ]
REDIS_SET_CMDS = ['set', 'mset', 'hmset', 'hset', 'lset', 'getset', 'msetnx', 'psetex', 'setbit',
                  'setex', 'setnx', 'setrange', 'hsetnx']
REDIS_GET_CMDS = ['get', 'getbit', 'getrange',
    'mget', 'hget', 'hgetall', 'hmget']
REDIS_KEY_BASED_CMDS = ['del', 'dump', 'exists', 'expire', 'expireat', 'keys', 'migrate', 'move',
                        'object', 'persist', 'pexpire', 'pexpireat', 'pttl', 'randomkey', 'rename',
                        'renamenx', 'restore', 'sort', 'ttl', 'type', 'scan']
REDIS_STRING_BASED_CMDS = ['append', 'bitcount', 'bitop', 'bitpos', 'decr', 'decrby', 'get', 'getbit',
                           'getrange', 'getset', 'incr', 'incrby', 'incrbyfloat', 'mget', 'mset',
                           'msetnx', 'psetex', 'set', 'setbit', 'setex', 'setnx', 'setrange', 'strlen']
REDIS_HASH_BASED_CMDS = ['hdel', 'hexists', 'hget', 'hgetall', 'hincrby', 'hincrbyfloat', 'hkeys', 'hlen',
                         'hmget', 'hmset', 'hset', 'hsetnx', 'hvals', 'hscan']
REDIS_LIST_BASED_CMDS = ['blpop', 'brpop', 'brpoplpush', 'lindex', 'linsert', 'llen', 'lpop', 'lpush',
                         'lpushx', 'lrange', 'lrem', 'lset', 'ltrim', 'rpop', 'rpoplpush', 'rpush',
                         'rpushx']
REDIS_SET_BASED_CMDS = ['sadd', 'scard', 'sdiff', 'sdiffstore', 'sinter', 'sinterstore', 'sismember',
                        'smembers', 'smove', 'spop', 'srandmember', 'srem', 'sunion', 'sunionstore',
                        'sscan']
REDIS_SORTED_SET_BASED_CMDS = ['zadd', 'zcard', 'zcount', 'zincrby', 'zinterstore', 'zlexcount', 'zrange',
                               'zrangebylex', 'zrevrangebylex', 'zrangebyscore', 'zrank', 'zrem', 'zremrangebylex',
                               'zremrangebyrank', 'zremrangebyscore', 'zrevrange', 'zrevrangebyscore', 'zrevrank',
                               'zscore', 'zunionstore', 'zscan']
REIDS_DBS = ['db0', 'db1', 'db2', 'db3', 'db4', 'db5', 'db6', 'db7',
    'db8', 'db9', 'db10', 'db11', 'db12', 'db13', 'db14', 'db15']


class Monitor:

    def __init__(self, host="localhost", port=6379, require_pass=False, password=None):
        self.host = host
        self.port = port
        self.require_pass = require_pass
        self.password = password
        self.rd = None

    def __connect_to_server(self):

        if self.require_pass and self.password is None:
            print "Password required"
            return

        try:
            if self.require_pass:
                self.rd = redis.StrictRedis(host=self.host, port=self.port, password=self.password)
            else:
                self.rd = redis.StrictRedis(host=self.host, port=self.port)
        except redis.exceptions.ResponseError:
            print "Can not connect to redis server"

    def __save_to_file(self, values):
        if os.path.isfile(Constants.MONITOR_FILE):
            open(Constants.MONITOR_FILE, "w").close()
    
        with open(Constants.MONITOR_FILE, "w") as outfile:
            json.dump(values, outfile)

    def __load_from_file(self):
        if os.path.isfile(Constants.MONITOR_FILE):
            with open(Constants.MONITOR_FILE, "r") as inputfile:
                return json.load(inputfile)
        return {}

    def collect_data(self):
        self.__connect_to_server()
        try:
            info = self.rd.info("ALL")
        except:
            return {}

        values = {}
        key_count = 0
        get_count = 0
        set_count = 0
        key_based_count = 0
        string_based_count = 0
        set_based_count = 0
        sorted_set_based_count = 0
        list_based_count = 0
        hash_based_count = 0
        max_memory = info.get("maxmemory", 0)
        used_memory = info.get('used_memory', 0)
        memory_usage = 0

        for k, v in info.iteritems():
            # print k, v
            if k.startswith("cmdstat_"):
                items = k.split('_')
                # print k, v, v['calls']
                if len(items) != 2:
                    continue

                if items[1] in REDIS_GET_CMDS:
                    get_count += int(v["calls"])
                elif items[1] in REDIS_SET_CMDS:
                    set_count += int(v["calls"])
                elif items[1] in REDIS_KEY_BASED_CMDS:
                    key_based_count += int(v["calls"])
                elif items[1] in REDIS_STRING_BASED_CMDS:
                    string_based_count += int(v["calls"])
                elif items[1] in REDIS_SET_BASED_CMDS:
                    set_based_count += int(v["calls"])
                elif items[1] in REDIS_SORTED_SET_BASED_CMDS:
                    sorted_set_based_count += int(v["calls"])
                elif items[1] in REDIS_LIST_BASED_CMDS:
                    list_based_count += int(v["calls"])
                elif items[1] in REDIS_HASH_BASED_CMDS:
                    hash_based_count += int(v["calls"])
            elif k in REDIS_STATIC_KEYS:
                values[k] = v
            elif k in REIDS_DBS:
                key_count += int(v["keys"])

        if max_memory <= 0:
            memory_usage = 0
        else:
            memory_usage = round(((float)(used_memory) / max_memory) * 1000, 1)
            memory_usage = int(memory_usage * 10)

        memory_usage = 1000 if memory_usage > 1000 else memory_usage

        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        hit_rate = 0

        if keyspace_hits == 0 and keyspace_misses == 0:
            hit_rate = 0
        else:
            hit_rate = round(((float)(keyspace_hits) / (keyspace_hits + keyspace_misses)) * 100, 1)
            hit_rate = int(hit_rate * 10)

        values['memory_usage_min'] = memory_usage
        values['memory_usage_avg'] = memory_usage
        values['memory_usage_max'] = memory_usage
        values['hit_rate_min'] = hit_rate
        values['hit_rate_avg'] = hit_rate
        values['hit_rate_max'] = hit_rate
        values['set_count'] = set_count
        values['get_count'] = get_count
        values['key_based_count'] = key_based_count
        values['string_based_count'] = string_based_count
        values['set_based_count'] = set_based_count
        values['sorted_set_based_count'] = sorted_set_based_count
        values['list_based_count'] = list_based_count
        values['hash_based_count'] = hash_based_count
        values['key_count'] = key_count
        
        if 'connected_clients' in values:
            values['connected_clients_min'] = values['connected_clients']
            values['connected_clients_avg'] = values['connected_clients']
            values['connected_clients_max'] = values['connected_clients']

        return values

if __name__=="__main__":

    host = "localhost"
    port = 6379
    password = None
    require_pass = False

    if len(sys.argv) == 2:
        password = sys.argv[1]

    monitor = Monitor(host=host, port=port, require_pass=True, password="Pa88w0rd")
    print json.dumps(monitor.collect_data())
