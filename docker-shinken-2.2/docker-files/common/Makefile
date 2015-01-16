DOCKER=/usr/bin/docker
DOCKERENTER=/usr/bin/docker-enter
IMAGE=$(REPO)/$(NAME):$(TAG)
REPO=shinken

clean:
	- @echo "Remove container $(RUNNAME)"
	- @$(DOCKER) rm $(RUNNAME) > /dev/null 2>&1
	- @echo "Remove image $(IMAGE)"
	- @$(DOCKER) rmi $(IMAGE) > /dev/null 2>&1
	- @echo "Remove orphaned images"
	- @$(DOCKER) rmi $$($(DOCKER) images |grep "none" |awk '{print $$3'})

build: 
	$(DOCKER) build --force-rm -t $(IMAGE) .

rebuild: 
	$(DOCKER) build --no-cache --rm --force-rm -t $(IMAGE) .


run:
	JOB=$$($(DOCKER) run -v /etc/localtime:/etc/localtime:ro --name $(RUNNAME) $(IMAGE) > /dev/null 2>&1 &)

interactive:
	$(DOCKER) run -ti --rm -v /etc/localtime:/etc/localtime:ro --name $(RUNNAME) $(IMAGE) $(SHELL)

start:
	$(DOCKER) start $(RUNNAME) 

stop:
	$(DOCKER) stop $(RUNNAME) 

enter:
	$(DOCKERENTER) $(RUNNAME)

ip:
	@$(DOCKER) inspect --format='{{.NetworkSettings.IPAddress}}' $(RUNNAME)

rm:
	$(DOCKER) rm $(RUNNAME)

push:
	$(DOCKER) login -u $(REPO)
	$(DOCKER) push $(IMAGE)

.PHONY: clean build rebuild run start stop enter ip interactive rm push

