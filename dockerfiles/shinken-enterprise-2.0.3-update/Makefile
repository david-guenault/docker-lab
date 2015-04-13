include ../common/Makefile
NAME = ske
RUNNAME = ske
TAG = 2.03-update
DOCKER=/usr/bin/docker

rebuild:
	@-$(MAKE) kill
	@-$(MAKE) rm
	@-$(MAKE) clean
	$(MAKE) build

startske:
	$(DOCKER) run -d --name $(RUNNAME) --hostname $(RUNNAME) -p 7766:7766 -p 7767:7767 $(IMAGE)