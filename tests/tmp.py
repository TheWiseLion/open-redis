from open_redis.deployment import RedisDeployment

procs = RedisDeployment.list_running_instances()
for proc in procs:
    proc.stop()

RedisDeployment('~/redis-test').start()
RedisDeployment('~/redis-test').stop()
RedisDeployment('~/redis-test').start()

