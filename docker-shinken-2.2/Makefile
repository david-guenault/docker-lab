TAG=2.2
PROJECT=shinken22
FIG=/usr/local/bin/fig
DOCKER=/usr/bin/docker
DOCKERENTER=/usr/bin/docker-enter

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

.PHONY: clean build kill rm rebuild start stop enter