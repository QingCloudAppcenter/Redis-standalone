#!/usr/bin/python


DATA_HOME = "/data/redis"
MASTER_FILE = DATA_HOME + "/master"
MONITOR_FILE = DATA_HOME + "/monitor.json"
REDIS_HOME = "/opt/redis"
SENTINEL_PORT = 26379
REDIS_SENTINEL_NAME = "master"
QUORUM = 2
MAX_MEMORY_PERCENTAGE = 0.8
AUTHORIZED_KEYS_FILE = "/root/.ssh/authorized_keys"
AUTHORIZED_KEYS_FILE_BACKUP = "/root/.ssh/authorized_keys.backup"

DISABLE_ALL = "DISABLE_ALL"
DISABLE_COMMANDS = ["CONFIG", "BGREWRITEAOF", "BGSAVE", "DEBUG", "SAVE", "SHUTDOWN", "SLAVEOF"]

DEFAULT_CONFIGS = {
    'appendonly': 'yes', 
    'zset-max-ziplist-entries': '128', 
    'zset-max-ziplist-value': '64', 
    'slave-serve-stale-data': 'yes', 
    'slave-priority': '0', 
    'rdbchecksum': 'yes', 
    'port': '6379', 
    'appendfsync': 'everysec', 
    'aof-rewrite-incremental-fsync': 'yes', 
    'list-max-ziplist-entries': '512', 
    'set-max-intset-entries': '512', 
    'lua-time-limit': '5000',
    'slowlog-log-slower-than': '-1', 
    'slowlog-max-len': '128', 
    'latency-monitor-threshold': '0', 
    'activerehashing': 'yes', 
    'save': '""', 
    'rdbcompression': 'yes', 
    'pidfile': '/var/run/redis/redis-server.pid', 
    'auto-aof-rewrite-percentage': '10', 
    'hz': '10', 
    'list-max-ziplist-value': '64', 
    'repl-disable-tcp-nodelay': 'no', 
    'hash-max-ziplist-entries': '512', 
    'dbfilename': 'dump.rdb', 
    'slave-read-only': 'yes', 
    'client-output-buffer-limit normal': '0 0 0', 
    'client-output-buffer-limit pubsub': '32mb 8mb 60', 
    'client-output-buffer-limit slave': '256mb 64mb 60', 
    'auto-aof-rewrite-min-size': '64mb', 
    'stop-writes-on-bgsave-error': 'yes', 
    'hash-max-ziplist-value': '64', 
    'logfile': '%s/logs/redis-server.log' % DATA_HOME,
    'tcp-keepalive': '0', 
    'no-appendfsync-on-rewrite': 'yes', 
    'loglevel': 'notice', 
    'hll-sparse-max-bytes': '3000', 
    'notify-keyspace-events': '""', 
    'appendfilename': '"appendonly.aof"', 
    'daemonize': 'yes', 
    'timeout': '0', 
    'databases': '16', 
    'tcp-backlog': '511',  
    'dir': DATA_HOME,
    'bind': '0.0.0.0',
    'maxclients': 65535,
    'requirepass' :'',
    'maxmemory-policy': 'volatile-lru',
    'maxmemory-samples': 3,
    'min-slaves-max-lag': 10,
    'min-slaves-to-write': 0,
    'repl-backlog-size': 1048576,
    'repl-backlog-ttl': 3600,
    'repl-timeout': 60,
}