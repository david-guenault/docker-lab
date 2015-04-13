include ../common/Makefile
NAME = shinken-thruk
RUNNAME = shinken-thruk
TAG = latest
DOCKER=/usr/bin/docker

rebuild:
	@-$(MAKE) kill
	@-$(MAKE) rm 
	@-$(MAKE) clean
	$(MAKE) build

startshinken:
	$(DOCKER) run -d --name $(RUNNAME) --hostname $(RUNNAME) -p 80:80 -p 7767:7767 -p 8086:8086 -p 8083:8083 -p 3000:3000 $(IMAGE)

stopshinken:
	$(DOCKER) stop $(RUNNAME)

