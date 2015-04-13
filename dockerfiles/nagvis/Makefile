include ../common/Makefile
NAME = nagvis
RUNNAME = nagvis
TAG = latest
DOCKER=/usr/bin/docker

rebuild:
	@-$(MAKE) kill
	@-$(MAKE) rm 
	@-$(MAKE) clean
	$(MAKE) build

startshinken:
	$(DOCKER) run -d --name $(RUNNAME) --hostname $(RUNNAME) -p 80:80 $(IMAGE)

stopshinken:
	$(DOCKER) stop $(RUNNAME)
