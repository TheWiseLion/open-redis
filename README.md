# open-redis [![Build Status](https://travis-ci.org/TheWiseLion/open-redis.svg?branch=master)](https://travis-ci.org/TheWiseLion/open-redis)
#### *A python package to help install, launch, and manage redis* ####

### Requirements ###
To install you need some form gcc compiler installed on the operating system beforehand.
Currently this package does not work for windows.

### Installation ###
This package can be installed from [PyPy](https://pypi.python.org/pypi?:action=display&name=open-redis)

* RHEL:
    ```bash
    yum group install "Development Tools"
    ```
* Ubuntu:



### Usage ###
  * #### Command Line #### 
    You can use redis-express to run a local redis server.
    ```bash
    $ redis-express -h
    usage: redis-express [-h] -d DEPLOY_FOLDER [-c [CONFIG_FILE]] [-p [PORT]]
    
    A commandline utility to launch redis. All output (e.g. logs, dumps, etc) will
    go into the chosen deployment folder (unless overridden)
    
    optional arguments:
      -h, --help            show this help message and exit
      -d DEPLOY_FOLDER, --deploy_folder DEPLOY_FOLDER
                            Folder to deploy to
      -c [CONFIG_FILE], --config_file [CONFIG_FILE]
                            Path to additional configuration file
      -p [PORT], --port [PORT]
                            The port to start the server on
                            
                            
                            
    $ redis-express -d ~/demo -p 10000
    Redis install location: /home/ec2-user/test/lib/python2.7/site-packages/open_redis/redis-4.0.1/src/redis-server
    Using Redis Version: 4.0.1
                    _._
               _.-``__ ''-._
          _.-``    `.  `_.  ''-._           Redis 4.0.1 (00000000/0) 64 bit
      .-`` .-```.  ```\/    _.,_ ''-._
     (    '      ,       .-`  | `,    )     Running in standalone mode
     |`-._`-...-` __...-.``-._|'` _.-'|     Port: 10000
     |    `-._   `._    /     _.-'    |     PID: 31906
      `-._    `-._  `-./  _.-'    _.-'
     |`-._`-._    `-.__.-'    _.-'_.-'|
     |    `-._`-._        _.-'_.-'    |           http://redis.io
      `-._    `-._`-.__.-'_.-'    _.-'
     |`-._`-._    `-.__.-'    _.-'_.-'|
     |    `-._`-._        _.-'_.-'    |
      `-._    `-._`-.__.-'_.-'    _.-'
          `-._    `-.__.-'    _.-'
              `-._        _.-'
                  `-.__.-'
    
    31906:M 07 Sep 04:40:20.890 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
    31906:M 07 Sep 04:40:20.890 # Server started, Redis version 4.0.1
    31906:M 07 Sep 04:40:20.891 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
    31906:M 07 Sep 04:40:20.891 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
    31906:M 07 Sep 04:40:20.891 * The server is now ready to accept connections on port 10000
    ``` 
    
* #### Python ####
    A single or multiple servers can be started through python
    ```python
        import redis  # Common redis client
        from open_redis.deployment import RedisDeployment
        
        # Example of starting a server
        server = RedisDeployment('~/output_folder', port=7653)
        server.start()
        r = redis.StrictRedis(host='localhost', port=7653, db=0)
        r.set('test', 'me')
        r.get('test')
        
        # You can see local running servers with list running instances
        server = RedisDeployment.list_running_instances()[0]
        
        server.stop()
    ```
    
    There is also built in functionality for using Sentinels to maintain redis clusters
    ```python
        from redis.sentinel import Sentinel  # Common redis client
        from open_redis.deployment import RedisDeployment, RedisSentinel
        
        # Setup Master & Slave
        master = RedisDeployment('~/redis-test-daemon', port=3428)
        salve = RedisDeployment('~/redis-test-daemon', port=3429)

        master.start()
        salve.start(master_ip='127.0.0.1', master_port=3428)

        # Setup Sentinel
        sentinel = RedisSentinel('~/redis-test-daemon')
        sentinel.start(master_ip='127.0.0.1',master_port=3428, master_name='mymaster')

        ## len(RedisSentinel.list_running_instances()) == 1
        ## len(RedisDeployment.list_running_instances()) == 2

        # Client API
        sentinel = Sentinel([('localhost', sentinel.port)], socket_timeout=0.1)
        master_client = sentinel.master_for('mymaster')
        slave_client = sentinel.slave_for('mymaster')
        master_client.set('foo', 'bar')
        slave_client.get('foo')  # bar
    ```
    

### Confirmed Platforms ###
Tested on AWS EC2 Instances

Operating System  | Tested Versions |
-------------     | ------------- |
Ubuntu      | ?  |
Red Hat      | 5, 6, 7  |