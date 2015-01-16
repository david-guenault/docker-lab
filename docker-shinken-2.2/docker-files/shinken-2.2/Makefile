NAME = shinken
RUNNAME = shinken
TAG = 2.2

include ../common/Makefile

conf:
	- @rm -Rf config
	- @$(DOCKER) cp $(IMAGE):/etc/shinken ./config