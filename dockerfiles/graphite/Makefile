include ../common/Makefile
NAME = graphite
RUNNAME = graphite
TAG = latest
DOCKER=/usr/bin/docker



rebuild:
	@-$(MAKE) kill
	@-$(MAKE) rm
	@-$(MAKE) clean
	$(MAKE) build

startgraphite:
	$(DOCKER) run -d --name $(RUNNAME) --hostname $(RUNNAME) -p 8080:80 -p 2003:2003 -p 2004:2004 -p 7002:7002 $(IMAGE)

