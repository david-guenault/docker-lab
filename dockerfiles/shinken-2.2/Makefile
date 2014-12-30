NAME = shinken
RUNNAME = shinken
TAG = 2.2
IMGNAME = azertyqsdfgh


include ../common/Makefile

buildcompactconf:
	- @$(DOCKER) rm $(IMGNAME)
	- @$(DOCKER) run -ti --name $(IMGNAME) -v $(CURDIR)/files/compactconf.sh:/etc/shinken/compactconf.sh $(IMAGE)  /bin/bash /etc/shinken/compactconf.sh
	- @$(DOCKER) cp $(IMGNAME):/tmp/shinken-conf.cfg ./files/
	- @$(DOCKER) rm $(IMGNAME)