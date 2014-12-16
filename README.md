docker-lab
==========

Easyly build docker containers based labs. The main "drawback" with docker containers is to deal with ip address change at each reboot. 
There are solutions that help a lot with this but at a cost of complexity that is not productive at all for just building simple labs. 
Dock2dns just create and remove dnsentry in skydns2 each time you start/stop containers. 
This way communication between containers is as simple as just using a name. Say you have a container with hostname A and another with hostname B. If you want to ping A from B you just have to ping it like ping B. dock2dns just do the dns discovery job for you.

Docker lab use etcd and skydns2 as dynamic dns registration tool with the dock2dns.py script to detect envents from docker daemon. 

How to use it:
==============

Grab this github repo (you need docker and fig running on your host). Go to dock2dns folder and execute fig up -d command. That's it ! now you have a basic and simple dns discovery for all of your docker containers without modifying anything. 

```
git clone https://github.com/david-guenault/docker-lab
cd docker-lab/dock2dns
fig up -d
```

Now time to see if it works for real 

```
dig @172.17.42.1 SRV dock2dns.lan
...
;; ADDITIONAL SECTION:
skydns.dock2dns.lan.	3600	IN	A	172.17.0.199
etcd.dock2dns.lan.	3600	IN	A	172.17.0.197
...
```

Now start another container 

```
docker start -ti --rm --name bb --hostname bb busybox top
```

See in skydns2 that the bb dns entry is created 

```
dig @172.17.42.1 SRV dock2dns.lan
...
;; ADDITIONAL SECTION:
skydns.dock2dns.lan.	3600	IN	A	172.17.0.199
etcd.dock2dns.lan.	3600	IN	A	172.17.0.197
bb.dock2dns.lan.	3600	IN	A	172.17.0.205
```

Now stop the container and check that the entry is removed

```
docker stop bb
dig @172.17.42.1 SRV dock2dns.lan
...
;; ADDITIONAL SECTION:
skydns.dock2dns.lan.	3600	IN	A	172.17.0.199
etcd.dock2dns.lan.	3600	IN	A	172.17.0.197
```

That was pretty simple hu ? 

Modify domain 
=============

Well you do not want to use this dock2dns.lan domain name ? ok use your own !

```
fig stop
make clean && make config DOMAIN=mydomain.tld
fig up -d
dig @172.17.42.1 SRV mydomain.tld
...
;; ADDITIONAL SECTION:
etcd.mydomain.tld.	3600	IN	A	172.17.0.209
skydns.mydomain.tld.	3600	IN	A	172.17.0.211

```

That's it !

Build a lab
===========

Labs are based on fig (simple orchestration tool). Everything is defined in a single YAML file. Here is a simple example with 2 busybox containers that just run a top command

```
b1:
    image: busybox 
    name: b1 
    hostname: b1 
    volumes:
        - /etc/localtime:/etc/localtime:ro
        - resolv.conf:/etc/resolv.conf
    entrypoint: top

b2:
    image: busybox 
    name: b2 
    hostname: b2 
    volumes:
        - /etc/localtime:/etc/localtime:ro
        - resolv.conf:/etc/resolv.conf
    entrypoint: top
```

This one is already provided with the repo. Go to 2boxes folder and run the command:

```
fig up -d
```

Then see that it is running with the following command

```
fig ps
   Name       Command   State   Ports 
-------------------------------------
2boxes_b1_1   top       Up            
2boxes_b2_1   top       Up            
```

Enter the 2boxes_b1_1 container and check that it is resolved on 'mydomain.tld'

```
docker-enter 2boxes_b1_1
ping b2.mydomain.tld
PING b2.mydomain.tld (172.17.0.213): 56 data bytes
64 bytes from 172.17.0.213: seq=0 ttl=64 time=0.077 ms
64 bytes from 172.17.0.213: seq=1 ttl=64 time=0.064 ms
64 bytes from 172.17.0.213: seq=2 ttl=64 time=0.071 ms
64 bytes from 172.17.0.213: seq=3 ttl=64 time=0.071 ms
...
```

The secret behind the "magic" is that i provide a hostname to the container and i map a resolv.conf file as a volume. DNS name resolution in the container point to 172.17.42.1. 
