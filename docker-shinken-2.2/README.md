# Shinken 2.2 as a docker application

## Prerequisites:

### Docker 

You can find documentation about how to install docker at the following location

  - Debian : https://docs.docker.com/installation/debian/
  - Ubuntu : https://docs.docker.com/installation/ubuntulinux/
  - Redhat : https://docs.docker.com/installation/rhel/
  - Centos : https://docs.docker.com/installation/centos/

### Fig

Every gnu/linux flavor should work the same way. Fig is a python application and can be installed the following way (as root user): 
  
  ```
  pip install -U fig
  ```

### nsenter:
  
nsenter is released as a docker container that will put the binary where you want. The only required thing is that it need to be accessible in the PATH. Let say /usr/local/bin/nsenter

  ```
  docker run --rm jpetazzo/nsenter cat /nsenter > /tmp/nsenter 
  chmod +x /tmp/nsenter
  docker rmi jpetazzo/nsenter
  mv /tmp/nsenter /usr/local/bin/nsenter
  ```
nsenter come with a convenient script that make it more simple to use (docker-enter). We have to grab it and put it in a location that is available in the path

   ```
   wget https://raw.githubusercontent.com/jpetazzo/nsenter/master/docker-enter -O /usr/local/bin/docker-enter
   chmod +x /usr/local/bin/docker-enter
   ```

## Building the docker image

There is only one versatile docker image. You can build it by using the provided Makefile (install make before using it). The only thing needed to build the image is an access to internet (for Debian 7 mirror access).

```
make build
```

Once finished you can see that the image has been added to your docker images

```
docker images
REPOSITORY                      TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
shinken/shinken                 2.2                 10f9da402621        16 minutes ago      491.4 MB
```

## Quick Start

```
make build start
```

## Using

### Docker explained

Ok everything is now setup. Let start to use. Fig is a simple (but powerfull) orchestration tool for docker. Without fig you have to deal with a lot of docker commands, so fig is curently the most simple and efficient way to use multicontainer applications. With shinken we have 6 daemons, each responsible of a specific task. 

- arbiter load, parse and send the configuration to others daemons
- scheduler ... schedule the checks execution
- poller execute the check and send back results to the scheduler
- broker take monitoring data from the scheduler and send it to others backends (databases, metrology, webinterface ...)
- reactionner take alerting data and notify user (by email or sms for exemple)
- receiver is just a queue manager used to receive external commands

In a simple setup we have to launch 6 docker containers each with a specific command. For exemple the arbiter is launched the following way :

```
docker run -d --name arbiter1 --hostname arbiter1 -v /etc/localtime:/etc/localtime:ro -v $(pwd)/config/shinken:/etc/shinken shinken/shinken:2.2 /usr/bin/shinken-arbiter -c /etc/shinken/shinken.cfg
```

You will notice the following argument "-v $(pwd)/config/shinken:/etc/shinken". This mount the local config/shinken folder into the container at /etc/shinken. This way we can configure shinken without entering the container every time we recreate the container. Local pathes must be absolute path. This is why i prepend with $(pwd) that will result in an absolute path. 

With the same logic we can launch all of our containers 

```
docker run -d --name receiver1 --hostname receiver1 -v /etc/localtime:/etc/localtime:ro shinken/shinken:2.2 /usr/bin/shinken-receiver -c /etc/shinken/daemons/receiverd.ini
docker run -d --name scheduler1 --hostname scheduler1 -v /etc/localtime:/etc/localtime:ro shinken/shinken:2.2 /usr/bin/shinken-scheduler -c /etc/shinken/daemons/schedulerd.ini
docker run -d --name reactionner1 --hostname reactionner1 -v /etc/localtime:/etc/localtime:ro shinken/shinken:2.2 /usr/bin/shinken-reactionner -c /etc/shinken/daemons/reactionnerd.ini
docker run -d --name poller1 --hostname poller1 -v /etc/localtime:/etc/localtime:ro shinken/shinken:2.2 /usr/bin/shinken-poller -c /etc/shinken/daemons/pollerd.ini
docker run -d --name broker1 --hostname broker1 -v /etc/localtime:/etc/localtime:ro shinken/shinken:2.2 /usr/bin/shinken-broker -c /etc/shinken/daemons/brokerd.ini
docker run -d --name arbiter1 --hostname arbiter1 -v /etc/localtime:/etc/localtime:ro -v $(pwd)config/shinken:/etc/shinken  shinken/shinken:2.2 /usr/bin/shinken-arbiter -c /etc/shinken/shinken.cfg

```

Nice ! ... but this won't work ! sad but true ... Every time you start a container a new ip is defined in it (docker way). So if we look in the configuration file (poller-master.cfg for example) you will notice that we use the host name poller1. Arbiter have to send the poller configuration to poller1 but have no idea how to resolve it. We have to find a way to tell each daemon what is the ip of the others. Every time you launch a container docker mount /etc/hosts as a volume and add an entry in it. Let give an example

```
docker run -ti --rm busybox cat /etc/hosts
10.0.8.14   da9f29e9a50b
127.0.0.1   localhost
::1 localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

We just launched a busybox container and see what is inside the /etc/hosts file. docker take the name of the container and the ip and add an entry to the /etc/hosts file. The default name is the container id. 

```
docker ps -a | awk '{print $1}'
CONTAINER ID
0a738b0ac201
```

We need something more relevant. So just specify the hostname

```
docker run -ti --rm --name mycontainer1 --hostname mycontainer1 busybox cat /etc/hosts
10.0.8.16   mycontainer1
127.0.0.1   localhost
::1 localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```
Yeah !

Ok but now i need a two containers setup where C2 can resolve C1. Links are the answer ! First start a container in background (C1 for the moment). Links use the container name to establish the relation between two runings containers. 

```
docker run -d --name C1 --hostname C1 busybox top
```

Now start C2 container linked to C1

```
docker run -ti --hostname C2 --link C1:C1 busybox ping C1
PING C1 (10.0.8.17): 56 data bytes
64 bytes from 10.0.8.17: seq=0 ttl=64 time=0.234 ms
64 bytes from 10.0.8.17: seq=1 ttl=64 time=0.132 ms
64 bytes from 10.0.8.17: seq=2 ttl=64 time=0.097 ms
64 bytes from 10.0.8.17: seq=3 ttl=64 time=0.099 ms
```

And it just work !

Ok now we have to establish links between each shinken container. First we have to now which daemons talk to others. In the default setup here is the answer :

- arbiter talk to every others daemons (have to send configuration to every daemons). If arbiter is a spare it talk to every others daemon except the arbiter master.
- reactionner(s) talk to scheduler(s)
- poller(s) talk to scheduler(s)
- broker(s) talk to every other daemons except arbiter(s)
- receiver does not talk ;-)
- scheduler(s) does not talk ;-)

Now we can say in which order every daemons should start. 

- receiver (because it does not need to talk to others)
- scheduler (it does not talk to others daemons)
- reactionner
- poller
- broker
- arbiter

So back to our first example here is the good setup. 

```
docker run -d --name receiver1 --hostname receiver1 -v /etc/localtime:/etc/localtime:ro shinken/shinken:2.2 /usr/bin/shinken-receiver -c /etc/shinken/daemons/receiverd.ini
docker run -d --name scheduler1 --hostname scheduler1 -v /etc/localtime:/etc/localtime:ro shinken/shinken:2.2 /usr/bin/shinken-scheduler -c /etc/shinken/daemons/schedulerd.ini
docker run -d --name reactionner1 --hostname reactionner1 -v /etc/localtime:/etc/localtime:ro --link scheduler1:scheduler1 shinken/shinken:2.2 /usr/bin/shinken-reactionner -c /etc/shinken/daemons/reactionnerd.ini
docker run -d --name poller1 --hostname poller1 -v /etc/localtime:/etc/localtime:ro --link scheduler1:scheduler1 shinken/shinken:2.2 /usr/bin/shinken-poller -c /etc/shinken/daemons/pollerd.ini
docker run -d --name broker1 --hostname broker1 -v /etc/localtime:/etc/localtime:ro --link scheduler1:scheduler1 --link receiver1:receiver1 --link poller1:poller1 --link reactionner1:reactionner1 shinken/shinken:2.2 /usr/bin/shinken-broker -c /etc/shinken/daemons/brokerd.ini
docker run -d --name arbiter1 --hostname arbiter1 -v /etc/localtime:/etc/localtime:ro -v $(pwd)config/shinken:/etc/shinken  --link scheduler1:scheduler1 --link receiver1:receiver1 --link poller1:poller1 --link reactionner1:reactionner1 --link broker1:broker1 shinken/shinken:2.2 /usr/bin/shinken-arbiter -c /etc/shinken/shinken.cfg
```
And now everything is up and running. But what a pain in the ass if we just have to introduce more daemons ....

## Fig 

Fig achieve the same goal (and much more) but everything is defined in a comprehensive YAML file. See the fig.yml file for a complete example, but you can see a sample of the exemple right here: 

```
arbiter1:
    image: shinken/shinken:2.2
    hostname: arbiter1
    volumes:
        - /etc/localtime:/etc/localtime:ro
        - config/shinken:/etc/shinken
    links:
        - broker1
        - poller1
        - scheduler1
        - reactionner1
        - receiver1
    expose:
        - "7770"
    command: /usr/bin/shinken-arbiter -c /etc/shinken/shinken.cfg

broker1:
    image: shinken/shinken:2.2
    hostname: broker1
    volumes:
        - /etc/localtime:/etc/localtime:ro
    links:
        - scheduler1
        - poller1
        - reactionner1
        - receiver1
    expose:
        - "7772"
        - "50000"
    command: /usr/bin/shinken-broker -c /etc/shinken/daemons/brokerd.ini
```
Much more readable ! and much more usable, you can find how to control your project right after :

- fig up -d (this will create/recreate and start the project each time you launch the command)
- fig kill (kill every container in the project. Fast but hardcore)
- fig stop (stop the whole project)
- fig start (start a previously created project with fig up)
- fig ps (display a comprehensive list of the project containers)

```          
fig ps   
Name                           Command               State          Ports        
---------------------------------------------------------------------------------------------
dockershinken22_arbiter1_1       /usr/bin/shinken-arbiter - ...   Up      7770/tcp            
dockershinken22_broker1_1        /usr/bin/shinken-broker -c ...   Up      50000/tcp, 7772/tcp 
dockershinken22_poller1_1        /usr/bin/shinken-poller -c ...   Up      7771/tcp            
dockershinken22_reactionner1_1   /usr/bin/shinken-reactionn ...   Up      7769/tcp            
dockershinken22_receiver1_1      /usr/bin/shinken-receiver  ...   Up      7773/tcp            
dockershinken22_scheduler1_1     /usr/bin/shinken-scheduler ...   Up      7768/tcp  
```

## Adding daemons

Let say you want to test shinken scalability by adding a poller to your project. It is really easy. 

First you have to add the poller to the shinken configuration. Create a new file named config/shinken/pollers/poller2.cfg and add the following content. 

```
define poller {
    poller_name  poller2
    address         poller2
    port            7771
    spare               0   
    manage_sub_realms   0   
    min_workers         0   
    max_workers         0   
    processes_by_worker 256 
    polling_interval    1   
    timeout             3   
    data_timeout        120 
    max_check_attempts  3   
    check_interval      60  
    modules     
    use_ssl           0
    hard_ssl_name_check   0
    realm   All
}
```

Edit the fig.yml and add the following 

```
poller2:
    image: shinken/shinken:2.2
    hostname: poller2
    volumes:
        - /etc/localtime:/etc/localtime:ro
    links:
        - scheduler1
    expose:
        - "7771"
    command: /usr/bin/shinken-poller -c /etc/shinken/daemons/pollerd.ini
```

Don't forget to modify the definition of arbiter1 so it link to poller2

```
arbiter1:
    ...
    links:
        - broker1
        - poller1
        - poller2
        ...
```

Then you just have to start your project

```
fig up -d
```

And control that everything is up and running

```
fig ps
             Name                           Command               State          Ports        
---------------------------------------------------------------------------------------------
dockershinken22_arbiter1_1       /usr/bin/shinken-arbiter - ...   Up      7770/tcp            
dockershinken22_broker1_1        /usr/bin/shinken-broker -c ...   Up      50000/tcp, 7772/tcp 
dockershinken22_poller1_1        /usr/bin/shinken-poller -c ...   Up      7771/tcp            
dockershinken22_poller2_1        /usr/bin/shinken-poller -c ...   Up      7771/tcp            
dockershinken22_reactionner1_1   /usr/bin/shinken-reactionn ...   Up      7769/tcp            
dockershinken22_receiver1_1      /usr/bin/shinken-receiver  ...   Up      7773/tcp            
dockershinken22_scheduler1_1     /usr/bin/shinken-scheduler ...   Up      7768/tcp           
```

## Testing module without rebuilding everything

Say you want to test a release of a module (for example the broker module webui). It is possible to do it without rebuilding everything. You just have to use volumes. In shinken, modules are located in two specific places. The module itself is in /var/lib/shinken/modules/[modulename] and the configuration is located in /etc/shinken/modules/[modulename].cfg. Every module is located on a github repo at http://github.com/shinken-monitoring. webui sources are located at http://github.com/shinken-monitoring/mod-webui. 

Grab the sources in the project folder

```
git clone https://github.com/shinken-monitoring/mod-webui
```

Edit the fig.yml file and add the following volume to broker1 definition

```
- mod-webui/module:/var/lib/shinken/modules/webui
```

And add the following volume to arbiter1 definition

```
- mod-webui/etc/modules/webui.cfg:/etc/shinken/modules/webui.cfg
```

Next you have to edit shinken broker definition (config/shinken/etc/shinken/brokers/broker-master.cfg) and add the module to the module directive

```
modules     livestatus, webui
```

Start the project

```
fig up -d
```

You can verify that everything is working by opening a browser and point to http://broker1:7767 (if you have a browser on the host running docker. If not read the following).

## Add remote daemons

sometime you want to make a simple load distribution.

For this use case we will leverage an upcoming technology from docker, docker swarm. Docker swarm add the ability to use multihost containers (cluster of docker hosts). As it is an upcoming technology we must install it from source (and use docker with a version >= 1.4)

```
sudo apt-get install golang
mkdir ~/gocode; export GOPATH=~/gocode.
go get -u github.com/docker/swarm
sudo cp ~/gocode/bin/swarm /usr/local/bin/swarm
```

***Note: This take a long time and must be repeated on each docker hosts.***

Now swarm must access every single nodes that are parts of the cluster. You need to modify default start options and add the -H argument. Edit the /etc/default/docker file on each node add -H tcp://0.0.0.0:2375 to DOCKER_OPTS

We will see later that we can define running strategy with docker. For example (and that's what we need) the hability to run containers on a specific host or group of host. For simplicity we will tag the docker hosts with a simple tag. This is done in the /etc/default/docker file. 

- On node 10.10.0.5 add --label node=node1 to DOCKER_OPTS
- On node 10.20.0.21 add --label node=node2 to DOCKER_OPTS

Then restart docker on both nodes

```
sudo service docker restart
```

Now it's time to create the cluster. We use for this example a simple file discovery backend but it is possible to use consul, etcd or the hosted discovery service from docker. 

```
# from any docker host (or any host)
echo "10.10.0.5:2375" > /tmp/cluster
echo "10.20.0.21:2375" >> /tmp/cluster
swarm manage --discovery file:///tmp/cluster -H 10.10.0.5:2376
```

Now docker client must use the swarm manager ip/port. This is really simple by exporting the DOCKER_HOST environment variable. 

```
export DOCKER_HOST=10.10.0.5:2376
docker info
Containers: 1
Nodes: 2
frofx-GA-78LMT-S2P: 10.20.0.21:2375
n54l: 10.10.0.5:2375
```

