# Travis CI tests
import logging

import os
import unittest
from time import sleep

import redis
from redis.sentinel import Sentinel
from open_redis.deployment import RedisDeployment, RedisSentinel

file_dir = os.path.realpath(__file__).rsplit('/', 1)[0] + "/"


class TestRedisDeploy(unittest.TestCase):
    def setUp(self):
        for server in RedisDeployment.list_running_instances():
            server.stop()
        for server in RedisSentinel.list_running_instances():
            server.stop()
        sleep(1)  # TODO: make stop() blocking

    def test_start_stop(self):
        server = RedisDeployment('~/redis-test-client')
        server.start()
        sleep(1)  # TODO: make start() blocking
        server.stop()
        self.assertTrue(len(RedisDeployment.list_running_instances()) == 0)

    def test_start_stop_daemon(self):
        # This test also checks configs works
        RedisDeployment('~/redis-test-daemon', conf=file_dir + 'include-configs').start()
        sleep(1)
        RedisDeployment('~/redis-test-daemon', conf=file_dir + 'include-configs').stop()
        sleep(1)
        self.assertTrue(len(RedisDeployment.list_running_instances()) == 0)

    def test_client_connects(self):
        server = RedisDeployment('~/redis-test-client', port=7653)
        server.start()
        sleep(2)
        r = redis.StrictRedis(host='localhost', port=7653, db=0)
        self.assertTrue(r.set('test', 'me'))
        self.assertTrue(str(r.get('test').decode('utf-8')) == 'me')
        server.stop()

    def test_simple_sentinel(self):
        # Setup Master & Slave
        master = RedisDeployment('~/redis-master', port=3428)
        salve = RedisDeployment('~/redis-slave', port=3429)

        master.start()
        salve.start(master_ip='127.0.0.1', master_port=3428)

        # Setup Sentinel
        redis_sentinel = RedisSentinel('~/redis-sentinel')
        redis_sentinel.start(master_ip='127.0.0.1',master_port=3428, master_name='mymaster')

        sleep(3)
        ## len(RedisSentinel.list_running_instances()) == 1
        ## len(RedisDeployment.list_running_instances()) == 2

        # Client API
        sentinel = Sentinel([('localhost', redis_sentinel.port)], socket_timeout=0.1)
        master_client = sentinel.master_for('mymaster')
        slave_client = sentinel.slave_for('mymaster')
        master_client.set('foo', 'bar')
        slave_client.get('foo')  # bar

        self.assertTrue(len(RedisSentinel.list_running_instances()) == 1)
        self.assertTrue(len(RedisDeployment.list_running_instances()) == 2)
        self.assertTrue(str(slave_client.get('foo').decode('utf-8')) == 'bar')

        # Close down the servers
        master.stop()
        salve.stop()
        redis_sentinel.stop()

    def test_travis_runs(self):
        # derpy derpy town.
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
