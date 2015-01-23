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
	
	# launch a local manager
	$(DOCKER) -H tcp://$(LOCALDOCKERHOST):$(DOCKERPORT) run -d \
	--name $(SWARMIMAGENAME)-MANAGE-$(LOCALDOCKERHOST) \
	-p $(SWARMPORT):$(SWARMPORT) \
	$(SWARMIMAGE) \
	manage etcd://$(LOCALETCDHOST):$(ETCDPORTCLI)/v2/keys/swarm --H 0.0.0.0:$(SWARMPORT) 

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
		# echo "Stop swarm manage on node $$NODE"; \
		# $(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) stop $(SWARMIMAGENAME)-MANAGE-$$NODE; \
		# $(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) rm $(SWARMIMAGENAME)-MANAGE-$$NODE; \
	done;

	# stop local 
	-@for C in $(SWARMIMAGENAME)-MANAGE-$(LOCALDOCKERHOST) $(SWARMIMAGENAME)-AGENT-$(LOCALDOCKERHOST) $(ETCDIMAGENAME)-$(LOCALETCDHOST); \
	do \
		$(DOCKER) -H tcp://$(LOCALDOCKERHOST):$(DOCKERPORT) kill $$C; \
		$(DOCKER) -H tcp://$(LOCALDOCKERHOST):$(DOCKERPORT) rm $$C; \
	done;

######################################
# ADD/REMOVE NODES AFTER BOOTSTRAPPING
######################################
startmanager:

stopmanager:

addnode:
	echo "Adding node $NODE to cluster"
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
swarmimage:
	# build and push swarmimage to docker hub
	- @$(DOCKER) rmi $(SWARMIMAGE)
	$(SUDO) rm -Rf /tmp/swarm && \
	cd /tmp && \
	$(GIT) clone https://github.com/docker/swarm && \
	cd swarm && \
	$(DOCKER) build -t $(SWARMIMAGE) . 
	$(DOCKER) login
	$(DOCKER) push

swarmdeploy:
	# deploy swarm image on all nodes
	-@for NODE in $(NODES); \
	do \
		echo "Deploy $(SWARMIMAGE) on node $$NODE"; \
		$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) pull $(SWARMIMAGE); \
	done;

etcddeploy:
	# deploy etcd image on all nodes
	-@for NODE in $(NODES); \
	do \
		echo "Deploy $(ETCDIMAGE) on node $$NODE"; \
		$(DOCKER) -H tcp://$$NODE:$(DOCKERPORT) pull $(ETCDIMAGE); \
	done;

deploy: swarmdeploy etcddeploy


# swarmstop: swarmstopremote swarmstoplocal

# swarmstart: swarmstartlocal swarmstartremote

# ps:
# 	@-$(DOCKER) -H $(LOCALSWARMHOST) ps

# swarmstartlocal:
# 	# $(DOCKER) -H $(LOCALDOCKERHOST) run -d --name $(LOCALETCDNAME) --hostname $(LOCALETCDNAME) -p $(LOCALETCDCLIENTPORT):$(LOCALETCDCLIENTPORT) -p $(LOCALETCDANNOUNCEPORT):$(LOCALETCDANNOUNCEPORT) $(ETCDIMAGE) 
# 	$(DOCKER) -H $(LOCALDOCKERHOST) run -d --name $(LOCALSWARMNAME) --hostname $(LOCALSWARMNAME) -p $(SWARMPORT):$(SWARMPORT) $(SWARMIMAGE) manage $(SWARMHOSTS) -H 0.0.0.0:$(SWARMPORT)

# swarmstoplocal:
# 	$(DOCKER) -H $(LOCALDOCKERHOST) stop $(LOCALSWARMNAME)
# 	$(DOCKER) -H $(LOCALDOCKERHOST)  rm $(LOCALSWARMNAME)

# swarmstartremote:
# 	export DOCKER_HOST=$(LOCALSWARMHOST)  && $(COMPOSE) -p swarm -f $(SWARMBOOTSTRAP)  up -d

# swarmstopremote:
# 	export DOCKER_HOST=$(LOCALSWARMHOST)  && $(COMPOSE) -p swarm -f $(SWARMBOOTSTRAP)  stop && $(COMPOSE) -p swarm -f $(SWARMBOOTSTRAP) rm --force

# swarmrmremote: 
# 	- @export DOCKER_HOST=$(LOCALSWARMHOST)  && $(COMPOSE) -p swarm -f $(SWARMBOOTSTRAP) rm

# swarmcleanremote:
# 	- @export DOCKER_HOST=$(LOCALSWARMHOST)  && $(DOCKER) rm $$($(DOCKER) ps -qa)


# startproject:
# 	if ! -z "$(PROJECT)"; \
# 	then \
# 		export DOCKER_HOST=$(LOCALSWARMHOST)  && $(COMPOSE) -p $(PROJECT) -f $(PROJECT).yml  up -d; \
# 	fi;

# # update tools
# swarmupdatelocal:
# 	$(SUDO) rm -Rf /tmp/gocode && \
# 	mkdir /tmp/gocode && \
# 	export GOPATH=/tmp/gocode && \
# 	$(SUDO) -E go get -u github.com/docker/swarm

# swarmimage: 
# 	- @$(DOCKER) rmi $(SWARMIMAGE)
# 	$(SUDO) rm -Rf /tmp/swarm && \
# 	cd /tmp && \
# 	$(GIT) clone https://github.com/docker/swarm && \
# 	cd swarm && \
# 	$(DOCKER) build -t $(SWARMIMAGE) . 

# # compose
# composeupdate:
# 	cd /tmp && \
# 	$(SUDO) rm -Rf fig && \
# 	$(GIT) clone https://github.com/docker/fig && \
# 	cd fig && \
# 	$(SUDO) pip install -r requirements.txt && \
# 	$(SUDO) pip install -r requirements-dev.txt && \
# 	$(SUDO) python setup.py develop

# deployimages:
# 	for image in $(IMAGELIST); \
# 	do \
# 		for host in $$(echo $(SWARMHOSTS) | sed -e "s/,/ /g"); \
# 		do \
# 			echo  "$$image => $$host"; \
# 			docker -H $$host pull $$image; \
# 		done; \
# 	done; 

.PHONY: swarmstart swarmstop ps swarmstartlocal swarmstoplocal swarmstartremote swarmstopremote deployimages

