######################################
# MODIFY WHAT YOU NEED HERE
######################################
# The domain Name to be used
DOMAIN=dock2dns.lan
DNSFORWARD=8.8.8.8:53
# DOCKER NODES
LOCAL=node1
NODES=node2 node3
# DOCKER HOSTS / PORTS
LOCALDOCKERHOST=$(LOCAL)
DOCKERPORT=2375
SWARMPORT=2376
# REMOTE NODES HOSTS
MANAGERSNODES=$(LOCAL) $(NODES)
CONSULNODES=$(LOCAL) $(NODES)
CONSULHTTPPORT=8500
# CERTIFICATES PATH
SWARMCERTS=/etc/pki/swarm
DOCKERCERTS=/etc/pki/docker
CLIENTCERTS=~/.docker
# DOCKER OPTIONS
DOCKERDAEMONIZE= -ti --rm 
DOCKER0=172.17.42.1
######################################
# DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING !
######################################
# BINARIES
DOCKER=/usr/bin/docker
COMPOSE=/usr/local/bin/docker-compose
GIT=/usr/bin/git
SUDO=/usr/bin/sudo
CAT=/bin/cat
# DOCKER HUB REPO
REPOSITORY=dguenault
# SWARM
SWARMIMAGENAME=swarm
SWARMREPO=docker
SWARMTAG=test
SWARMIMAGE=$(REPOSITORY)/$(SWARMIMAGENAME):$(SWARMTAG)
# MANAGERTLS=--tlsverify --tlscacert $(SWARMCERTS)/ca.pem --tlscert $(SWARMCERTS)/cert.pem --tlskey $(SWARMCERTS)/key.pem
# MANAGERTLSVOLUME= -v $(SWARMCERTS):/tlscerts
# CONSUL
CONSULDC=box4prod
CONSULIMAGENAME=consul
CONSULTAG=0.4.1
CONSULIMAGE=$(REPOSITORY)/$(CONSULIMAGENAME):$(CONSULTAG)

help:
	@-echo "TODO !"

##########################################################
# GLOBAL 
##########################################################

bootstart: startconsul registernodes startmanager

bootstop: stopmanager stopconsul 

##########################################################
# CONSUL
##########################################################

startconsul:
	@-IP=$$(ping -c 1 $(LOCAL) | head -n 1 | awk '{print $$3}' | sed -e "s/(//g" -e "s/)//g"); \
	ALLNODES=" $(LOCAL) $(NODES)"; \
	NODECOUNT=$$(echo $$ALLNODES | wc -w); \
	for NODE in $$ALLNODES; \
	do \
		NODEIP=$$(ping -c 1 $$NODE | head -n 1 | awk '{print $$3}' | sed -e "s/(//g" -e "s/)//g"); \
		$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) run -d \
			--name consul-$$NODE \
			--hostname consul-$$NODE \
			-p 8300:8300 \
			-p 8301:8301/udp \
			-p 8301:8301 \
			-p 8302:8302/udp \
			 -p 8302:8302 \
			 -p 8400:8400 \
			 -p 8500:8500 \
			 -p $(DOCKER0):53:8600/udp \
			 $(CONSULIMAGE) \
			 	agent \
			 	-server -data-dir /tmp/consul \
				-config-file /tmp/consul.cfg  \
			 	-node consul-$$NODE  \
			 	-bootstrap-expect $$NODECOUNT  \
			 	-bind 0.0.0.0  \
			 	-dc $(CONSULDC)  \
			 	-client 0.0.0.0 \
			 	-advertise $$NODEIP \
			 	-retry-join $$IP \
			 	-retry-interval 5s; \
		sleep 3; \
	done;

stopconsul:
	@-ALLNODES="$(NODES) $(LOCAL)"; \
	for NODE in $$ALLNODES; \
	do \
		echo "Stop consul on node $$NODE"; \
		$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) stop $(CONSULIMAGENAME)-$$NODE; \
		$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) rm $(CONSULIMAGENAME)-$$NODE; \
	done;

stopconsulnode:
	echo "Stop consul on node $$NODE"; \
	$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) stop $(CONSULIMAGENAME)-$$NODE; \

startconsulnode:
	echo "Start consul on node $$NODE"; \
	$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) start $(CONSULIMAGENAME)-$$NODE; \

createconsulnode:
	echo "Create consul node consul-$(NAME) on node $(NODE)"; \
	@-IP=$$(ping -c 1 $(NODE) | head -n 1 | awk '{print $$3}' | sed -e "s/(//g" -e "s/)//g"); \
	ALLNODES=" $(LOCAL) $(NODES)"; \
	NODECOUNT=$$(echo $$ALLNODES | wc -w); \
	$(DOCKER) -H tcp://$(NODE):$(DOCKERPORT) run -d \
		--name consul-$(NODE) \
		--hostname consul-$(NAME) \
		-p 8300:8300 \
		-p 8301:8301/udp \
		-p 8301:8301 \
		-p 8302:8302/udp \
		 -p 8302:8302 \
		 -p 8400:8400 \
		 -p 8500:8500 \
		 -p $(DOCKER0):53:8600/udp \
		 $(CONSULIMAGE) \
		 	agent \
		 	-server -data-dir /tmp/consul \
			-config-file /tmp/consul.cfg  \
		 	-node consul-$(NAME)  \
		 	-bootstrap-expect $$NODECOUNT  \
		 	-bind 0.0.0.0  \
		 	-dc $(CONSULDC)  \
		 	-client 0.0.0.0 \
		 	-advertise $$NODEIP \
		 	-retry-join $$IP \
		 	-retry-interval 5s; \


##########################################################
# SWARM NODE REGISTER
##########################################################

registernodes:
	PEERSCLI=""; \
	LOCALIP=$$(ping -c 1 $(LOCAL) | head -n 1 | awk '{print $$3}' | sed -e "s/(//g" -e "s/)//g"); \
	ALLNODES="$(LOCAL) $(NODES)"; \
	for NODE in $$ALLNODES; \
	do \
		IP=$$(ping -c 1 $$NODE | head -n 1 | awk '{print $$3}' | sed -e "s/(//g" -e "s/)//g"); \
		PEERSCLI="$$PEERSCLI,$$IP:$(CONSULHTTPPORT)"; \
	done; \
	PEERSCLI=$$(echo $$PEERSCLI | sed 's/^.//'); \
	for NODE in $$ALLNODES; \
	do \
		IP=$$(ping -c 1 $$NODE | head -n 1 | awk '{print $$3}' | sed -e "s/(//g" -e "s/)//g"); \
		echo "Starting swarm join on node $$NODE"; \
		$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) run -d \
		--name $(SWARMIMAGENAME)-AGENT-$$NODE \
		$(SWARMIMAGE) \
		join consul://$$PEERSCLI/swarm --addr $$IP:$(DOCKERPORT); \
		sleep 2; \
		$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) kill $(SWARMIMAGENAME)-AGENT-$$NODE; \
		$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) rm $(SWARMIMAGENAME)-AGENT-$$NODE; \
	done; 


######################################
# SWARM MANAGER
######################################
startmanager:
	@-echo "Start manager on $(NODE)"; \
	PEERSCLI=""; \
	LOCALIP=$$(ping -c 1 $(LOCAL) | head -n 1 | awk '{print $$3}' | sed -e "s/(//g" -e "s/)//g"); \
	ALLNODES="$(LOCAL) $(NODES)"; \
	for NODE in $$ALLNODES; do \
		IP=$$(ping -c 1 $$NODE | head -n 1 | awk '{print $$3}' | sed -e "s/(//g" -e "s/)//g"); \
		PEERSCLI="$$PEERSCLI,$$IP:$(CONSULHTTPPORT)"; \
	done;  \
	PEERSCLI="$$LOCALIP:$(CONSULHTTPPORT)$$PEERSCLI"; \
	$(DOCKER) -H tcp://$(NODE):$(DOCKERPORT) run -d \
		--name manager-$(NODE) \
		-p $(SWARMPORT):$(SWARMPORT) $(MANAGERTLSVOLUME) \
		$(SWARMIMAGE) \
		manage consul://$$PEERSCLI/swarm $(MANAGERTLS)  -H 0.0.0.0:$(SWARMPORT) 

stopmanager:
	@-echo "Stop manager on $(NODE)"
	@-$(DOCKER) -H tcp://$(NODE):$(DOCKERPORT) stop manager-$(NODE)
	@-$(DOCKER) -H tcp://$(NODE):$(DOCKERPORT) rm manager-$(NODE)

######################################
# HERE ARE IMAGES PREREQUISITES DEPLOYMENT
######################################

swarmimage:
	# build swarmimage 
	$(SUDO) rm -Rf /tmp/swarm && \
	cd /tmp && \
	$(GIT) clone https://github.com/$(SWARMREPO)/swarm && \
	- @$(DOCKER) -H $(LOCALDOCKERHOST):$(DOCKERPORT) rmi $(SWARMIMAGE)
	cd swarm && \
	if [ "$(SWARMTAG)" != "latest" ]; then $(GIT) checkout tags/$(SWARMTAG); fi && \
	$(DOCKER) -H $(LOCALDOCKERHOST):$(DOCKERPORT) build -t $(SWARMIMAGE) . 

swarmdevimage:
	cd go/src/github.com/docker/swarm && \
	$(DOCKER) -H $(LOCALDOCKERHOST):$(DOCKERPORT) build -t $(SWARMIMAGE) . 

swarmpush:
	$(DOCKER) -H $(LOCALDOCKERHOST):$(DOCKERPORT) login
	$(DOCKER) -H $(LOCALDOCKERHOST):$(DOCKERPORT) push $(SWARMIMAGE)

swarmdeploy:
	-@for NODE in $(NODES); \
	do \
		echo "Deploy $(SWARMIMAGE) on node $$NODE"; \
		$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) pull $(SWARMIMAGE); \
	done;

consulimage:
	cd ../dockerfiles/consul && \
	$(DOCKER) -H tcp://$(LOCAL):$(DOCKERPORT) build -t $(CONSULIMAGE) .

consulpush:
	$(DOCKER) -H tcp://$(LOCAL):$(DOCKERPORT) login
	$(DOCKER) -H tcp://$(LOCAL):$(DOCKERPORT) push $(CONSULIMAGE)

consuldeploy:
	-@for NODE in $(NODES); \
	do \
		echo "Deploy $(CONSULIMAGE) on node $$NODE"; \
		$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) pull $(CONSULIMAGE); \
	done;

.PHONY: 

