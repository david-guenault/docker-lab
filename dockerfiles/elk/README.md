<img src="https://docs.docker.com/img/nav/docker-logo-loggedin.png"> ELK Stack

<img src="http://download.redis.io/logocontest/82.png" height="60px"> <img src="http://logstash.net/images/logstash.png" height="60px"> <img src="http://www.laplagedigitale.eu/wp-content/uploads/2013/09/eslogo.png" height="60px">

### Presentation

This is a simple way to test the ELK stack as a centralized server. Every events are sents to the redis server, the logstash agent take the events in redis and send them to elasticserch. 

### Building

You will need at least docker, make tool and nsenter. Checkout the repo and launch the following command in a terminal. 

```make build```

### Starting (First time run)

just issue the following command to start the container in background. Note that this is only usefull for starting the container the first time

```make run```

Check that the container is running

```docker ps```

```CONTAINER ID        IMAGE                    COMMAND                CREATED             STATUS              PORTS                                  NAMES```

```47b687d69beb        dguenault/elk:1.0-beta   supervisord -c /etc   39 minutes ago      Up 39 minutes       9200/tcp, 9300/tcp, 6379/tcp, 80/tcp   elk-1.0-beta```

### Control container

* Stop container : make stop
* Start container : make start

### Control the daemons 

Daemons are controled by supervisord. If you want to start/stop/restart daemons (redis, elasticsearch, httpd, logstash), use the following command to access the supervisord web interface. 

```make supervisor```

Note : username is admin and password is supervisor

Note : you may want to customize your browser path in the Makefile by modifying the BROWSER variable. 

### Cleanup

If you want to remove everything (image and container) just run the following command :

```make clean```
