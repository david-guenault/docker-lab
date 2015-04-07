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
	$(DOCKER) run -d --name $(RUNNAME) --hostname $(RUNNAME) -p 80:80 -p 7767:7767 $(IMAGE)

stopshinken:
	$(DOCKER) stop $(RUNNAME)

