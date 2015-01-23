# BOOTSTRAP A DOCKER CLUSTER

## Quick start

- You need 3 dockers host (minimal cluster). Each configured with a running docker instance listening on [hostip]:[hostport]

- Configure the following variables in the Makefile 

```
# REMOTE NODES HOSTS
NODES=10.10.0.5 10.10.0.22
# ETCD HOSTS / PORTS
LOCALETCDHOST=10.20.0.21
ETCDPORTANN=7001
ETCDPORTCLI=4001
# DOCKER HOSTS / PORTS
LOCALDOCKERHOST=10.20.0.21
DOCKERPORT=2375
SWARMPORT=2376
```

- Build the required images (you need a docker hub account to push the images)

```
make images
```

- Deploy the required images

```
make deploy
```

- Bootstrap the cluster

```
make bootstart
```

- Stop the cluster

```
make bootstop
```

- run a swarm manage instance

```
make runmanager NODE=[dockerhostip]
export DOCKER_HOST=[dockerhostip]
docker ps -a
CONTAINER ID        IMAGE                    COMMAND                CREATED             STATUS              PORTS                                                  NAMES
cc7cf75c9c32        dguenault/swarm:latest   "swarm manage etcd:/   9 minutes ago       Up 9 minutes        2375/tcp, 10.20.0.21:2376->2376/tcp                    frofx-GA-78LMT-S2P/swarm-MANAGE-10.20.0.21   
74682316f46c        dguenault/swarm:latest   "swarm manage etcd:/   9 minutes ago       Up 9 minutes        2375/tcp, 10.10.0.22:2376->2376/tcp                    frogx-Vostro-3300/swarm-MANAGE-10.10.0.22    
521a40a80c40        dguenault/swarm:latest   "swarm manage etcd:/   10 minutes ago      Up 10 minutes       2375/tcp, 10.10.0.5:2376->2376/tcp                     n54l/swarm-MANAGE-10.10.0.5                  
c0e9af5967f9        dguenault/swarm:latest   "swarm join etcd://1   10 minutes ago      Up 10 minutes       2375/tcp                                               n54l/swarm-AGENT-10.10.0.5                   
e416d29130cf        dguenault/etcd:0.4.6     "/opt/etcd/bin/etcd    10 minutes ago      Up 10 minutes       10.10.0.5:4001->4001/tcp, 10.10.0.5:7001->7001/tcp     n54l/etcd-10.10.0.5                          
f0a4e6b5256f        dguenault/swarm:latest   "swarm join etcd://1   10 minutes ago      Up 10 minutes       2375/tcp                                               frofx-GA-78LMT-S2P/swarm-AGENT-10.20.0.21    
a182e0687231        dguenault/etcd:0.4.6     "/opt/etcd/bin/etcd    10 minutes ago      Up 10 minutes       10.20.0.21:4001->4001/tcp, 10.20.0.21:7001->7001/tcp   frofx-GA-78LMT-S2P/etcd-10.20.0.21           
cecd9eb133ac        dguenault/swarm:latest   "swarm join etcd://1   10 minutes ago      Up 10 minutes       2375/tcp                                               frogx-Vostro-3300/swarm-AGENT-10.10.0.22     
f99e973c0af5        dguenault/etcd:0.4.6     "/opt/etcd/bin/etcd    10 minutes ago      Up 10 minutes       10.10.0.22:4001->4001/tcp, 10.10.0.22:7001->7001/tcp   frogx-Vostro-3300/etcd-10.10.0.22 
```
- You are ready ! 