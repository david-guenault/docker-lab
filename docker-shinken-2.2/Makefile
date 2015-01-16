TAG=2.2
REPO=shinken
NAME=shinken
PROJECT=dockershinken22
FIG=/usr/local/bin/fig
DOCKER=/usr/bin/docker
DOCKERENTER=/usr/bin/docker-enter
IMAGE=$(REPO)/$(NAME):$(TAG)
ID=shinken22getconf

clean: 
	cd docker-files/shinken-$(TAG); \
	$(MAKE) $(TARGET);

build: 
	cd docker-files/shinken-$(TAG); \	
	$(MAKE) $(TARGET);

kill:
	$(FIG) kill

rm:
	$(FIG) rm --force

rebuild: kill rm clean build

restart:
	$(FIG) restart

start:
	$(FIG) up -d

stop:
	$(FIG) stop 

enter:
	$(DOCKERENTER) $(PROJECT)_$(DAEMON)_1

conf:
	docker run --name $(ID) $(IMAGE) echo
	- @rm -Rf config/*
	$(DOCKER) cp $(ID):/etc/shinken ./config/
	docker rm $(ID)

.PHONY: clean build kill rm rebuild start stop enter conf