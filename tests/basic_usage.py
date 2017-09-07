# Travis CI tests
import logging

import os
import unittest
from time import sleep

import redis
from open_redis.deployment import RedisDeployment, RedisSentinel

file_dir = os.path.realpath(__file__).rsplit('/', 1)[0] + "/"


class TestRedisDeploy(unittest.TestCase):
    def setUp(self):
        for server in RedisDeployment.list_running_instances():
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
        server = RedisDeployment('~/redis-test-daemon', conf=file_dir + 'include-configs').start()
        sentinel = RedisSentinel('~/redis-test-daemon')
        server.start()
        sentinel.start()
        self.assertTrue(len(RedisSentinel.list_running_instances()) == 1)
        sentinel.stop()
        server.stop()
        self.assertTrue(len(RedisSentinel.list_running_instances()) == 0)


    def test_travis_runs(self):
        # derpy derpy town.
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
