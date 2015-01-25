######################################
# MODIFY WHAT YOU NEED HERE
######################################
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
######################################
# DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING !
######################################
# BINARIES
DOCKER=/usr/bin/docker
COMPOSE=/usr/local/bin/docker-compose
GIT=/usr/bin/git
SUDO=/usr/bin/sudo
# DOCKER HUB REPO
REPOSITORY=dguenault
# SWARM
SWARMIMAGENAME=swarm
SWARMTAG=latest
SWARMIMAGE=$(REPOSITORY)/$(SWARMIMAGENAME):$(SWARMTAG)
# ETCD
ETCDIMAGENAME=etcd
ETCDTAG=0.4.6
ETCDIMAGE=$(REPOSITORY)/$(ETCDIMAGENAME):$(ETCDTAG)
ETCDHEARTHBEAT=10
# SKYDNS
SKYDNSIMAGENAME=skydns
SKYDNSTAG=latest
SKYDNSIMAGE=$(REPOSITORY)/$(SKYDNSIMAGENAME):$(SKYDNSTAG)

bootstart:
	# start a local etcd node that will act as the first master
	-@$(DOCKER) -H tcp://$(LOCALDOCKERHOST):$(DOCKERPORT) run -d \
	-p $(ETCDPORTANN):$(ETCDPORTANN) \
	-p $(ETCDPORTCLI):$(ETCDPORTCLI) \
	--name $(ETCDIMAGENAME)-$(LOCALETCDHOST) \
	$(ETCDIMAGE) \
	-peer-addr $(LOCALETCDHOST):$(ETCDPORTANN) -addr $(LOCALETCDHOST):$(ETCDPORTCLI) -data-dir machines/$(ETCDIMAGENAME)-$(LOCALETCDHOST) -name $(ETCDIMAGENAME)-$(LOCALETCDHOST)

	# make swarm join with etcd discovery backend
	-@$(DOCKER) -H tcp://$(LOCALDOCKERHOST):$(DOCKERPORT) run -d \
	--name $(SWARMIMAGENAME)-AGENT-$(LOCALDOCKERHOST) \
	$(SWARMIMAGE) \
	join etcd://$(LOCALETCDHOST):$(ETCDPORTCLI)/v2/keys/swarm --addr $(LOCALDOCKERHOST):$(DOCKERPORT) --hb $(ETCDHEARTHBEAT) 
	
	# start the cluster on all etcd nodes
	PEERSANN=""; \
	for NODE in $(NODES); \
	do \
		PEERSANN="$$PEERSANN,$$NODE:$(ETCDPORTCLI)"; \
	done; \
	PEERSANN=$(LOCALETCDHOST):$(ETCDPORTANN)$$PEERSANN; \
	for NODE in $(NODES); \
	do \
		echo "Starting etcd on node $$NODE"; \
		$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) run -d \
		-p $(ETCDPORTANN):$(ETCDPORTANN) \
		-p $(ETCDPORTCLI):$(ETCDPORTCLI) \
		--name $(ETCDIMAGENAME)-$$NODE \
		$(ETCDIMAGE) \
		-peer-addr $$NODE:$(ETCDPORTANN) -addr $$NODE:$(ETCDPORTCLI) --peers $$PEERSANN -data-dir machines/$(ETCDIMAGENAME)-$$NODE -name $(ETCDIMAGENAME)-$$NODE; \
	done; \
	for NODE in $(NODES); \
	do \
		echo "Starting swarm join on node $$NODE"; \
		$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) run -d \
		--name $(SWARMIMAGENAME)-AGENT-$$NODE \
		$(SWARMIMAGE) \
		join etcd://$$NODE:$(ETCDPORTCLI)/v2/keys/swarm --addr $$NODE:$(DOCKERPORT) --hb $(ETCDHEARTHBEAT) ; \
	done;

bootstop:
	# stop and clean remote etcd/swarmjoin/swarmmanage
	-@for NODE in $(NODES); \
	do \
		echo "Stop etcd on node $$NODE"; \
		$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) stop $(ETCDIMAGENAME)-$$NODE; \
		$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) rm $(ETCDIMAGENAME)-$$NODE; \
		echo "Stop swarm join on node $$NODE"; \
		$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) stop $(SWARMIMAGENAME)-AGENT-$$NODE; \
		$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) rm $(SWARMIMAGENAME)-AGENT-$$NODE; \
	done;

	# stop local 
	-@for C in $(SWARMIMAGENAME)-AGENT-$(LOCALDOCKERHOST) $(ETCDIMAGENAME)-$(LOCALETCDHOST); \
	do \
		$(DOCKER) -H tcp://$(LOCALDOCKERHOST):$(DOCKERPORT) kill $$C; \
		$(DOCKER) -H tcp://$(LOCALDOCKERHOST):$(DOCKERPORT) rm $$C; \
	done;

######################################
# ADD/REMOVE NODES AFTER BOOTSTRAPPING
######################################
startmanager:
	$(DOCKER) -H tcp://$(NODE):$(DOCKERPORT) run -d \
	--name $(SWARMIMAGENAME)-MANAGE-$(NODE) \
	-p $(SWARMPORT):$(SWARMPORT) \
	$(SWARMIMAGE) \
	manage etcd://$(NODE):$(ETCDPORTCLI)/v2/keys/swarm --H 0.0.0.0:$(SWARMPORT) 

stopmanager:
	$(DOCKER) -H tcp://$(NODE):$(DOCKERPORT) stop $(SWARMIMAGENAME)-MANAGE-$(NODE)
	$(DOCKER) -H tcp://$(NODE):$(DOCKERPORT) rm $(SWARMIMAGENAME)-MANAGE-$(NODE)

addnode:
	PEERSANN=""; \
	for NODEPEERS in $(NODES); \
	do \
		PEERSANN="$$PEERSANN,$$NODEPEERS:$(ETCDPORTCLI)"; \
	done; \
	PEERSANN=$(LOCALETCDHOST):$(ETCDPORTANN)$$PEERSANN; \
	echo "Starting etcd on node $(NODE)"; \
	$(DOCKER) -H tcp://$(NODE):$(DOCKERPORT) run -d \
	-p $(ETCDPORTANN):$(ETCDPORTANN) \
	-p $(ETCDPORTCLI):$(ETCDPORTCLI) \
	--name $(ETCDIMAGENAME)-$(NODE) \
	$(ETCDIMAGE) \
	-peer-addr $(NODE):$(ETCDPORTANN) -addr $(NODE):$(ETCDPORTCLI) --peers $$PEERSANN -data-dir machines/$(ETCDIMAGENAME)-$(NODE) -name $(ETCDIMAGENAME)-$(NODE); \
	echo "Starting swarm join on node $(NODE)"; \
	$(DOCKER) -H tcp://$(NODE):$(DOCKERPORT) run -d \
	--name $(SWARMIMAGENAME)-AGENT-$(NODE) \
	$(SWARMIMAGE) \
	join etcd://$(NODE):$(ETCDPORTCLI)/v2/keys/swarm --addr $(NODE):$(DOCKERPORT) --hb $(ETCDHEARTHBEAT);

removenode:
	echo "Removing node $NODE from cluster"
	$(DOCKER) -H tcp://$(NODE):$(DOCKERPORT) stop $(SWARMIMAGENAME)-AGENT-$(NODE); 
	$(DOCKER) -H tcp://$(NODE):$(DOCKERPORT) rm $(SWARMIMAGENAME)-AGENT-$(NODE); 
	$(DOCKER) -H tcp://$(NODE):$(DOCKERPORT) stop $(ETCDIMAGENAME)-$(NODE); 
	$(DOCKER) -H tcp://$(NODE):$(DOCKERPORT) rm $(ETCDIMAGENAME)-$(NODE); 

######################################
# HERE ARE IMAGES PREREQUISITES DEPLOYMENT
######################################
images: etcdimage swarmimage

swarmimage:
	# build and push swarmimage to docker hub
	- @$(DOCKER) -H $(LOCALDOCKERHOST):$(DOCKERPORT) rmi $(SWARMIMAGE)
	$(SUDO) rm -Rf /tmp/swarm && \
	cd /tmp && \
	$(GIT) clone https://github.com/docker/swarm && \
	cd swarm && \
	$(DOCKER) -H $(LOCALDOCKERHOST):$(DOCKERPORT) build -t $(SWARMIMAGE) . 
	$(DOCKER) -H $(LOCALDOCKERHOST):$(DOCKERPORT) login
	$(DOCKER) -H $(LOCALDOCKERHOST):$(DOCKERPORT) push $(SWARMIMAGE)

swarmdeploy:
	# deploy swarm image on all nodes
	-@for NODE in $(NODES); \
	do \
		echo "Deploy $(SWARMIMAGE) on node $$NODE"; \
		$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) pull $(SWARMIMAGE); \
	done;

etcdimage:
	# build and push etcd to docker hub
	- @$(DOCKER) -H $(LOCALDOCKERHOST):$(DOCKERPORT) rmi $(ETCDIMAGE)
	- @$(SUDO) rm -Rf /tmp/etcd && \
	cd /tmp && \
	$(GIT) clone https://github.com/coreos/etcd && \
	cd etcd && \
	$(GIT) checkout tags/v$(ETCDTAG) && \
	$(DOCKER) -H tcp://$(LOCALDOCKERHOST):$(DOCKERPORT) build -t $(ETCDIMAGE) . && \
	$(DOCKER) -H tcp://$(LOCALDOCKERHOST):$(DOCKERPORT) login && \
	$(DOCKER) -H tcp://$(LOCALDOCKERHOST):$(DOCKERPORT) push $(ETCDIMAGE)

etcddeploy:
	# deploy etcd image on all nodes
	-@for NODE in $(NODES); \
	do \
		echo "Deploy $(ETCDIMAGE) on node $$NODE"; \
		$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) pull $(ETCDIMAGE); \
	done;

cleanimages:
	-@for NODE in $(NODES); \
	do \
		echo "remove $(SWARMIMAGE) and $(ETCDIMAGE) on node $$NODE"; \
		$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) rmi $(SWARMIMAGE) $(ETCDIMAGE); \
	done;	


deploy: swarmdeploy etcddeploy

# swarm2dns 

.PHONY: bootstart bootstop startmanager stopmanager addnode removenode images swarmimage swarmdeploy etcdimage cleanimages etcddeploy

