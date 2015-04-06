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
	$(MAKE) run 
	sleep 2
	$(MAKE) ip 
	echo "http://$$($(MAKE) ip)/thruk/"
	$(MAKE) enter