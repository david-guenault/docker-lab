NAME = dock2dns
RUNNAME = dock2dns
TAG = latest

DOCKER=/usr/bin/docker
COMPOSE=/usr/local/bin/docker-compose
YAML=$(NAME).yml

include ../dockerfiles/common/Makefile

doup:
	$(COMPOSE) -f $(YAML)  up -d

dostart:
	$(COMPOSE) -f $(YAML) start

dostop:
	$(COMPOSE) -f $(YAML) stop

dokill:
	$(COMPOSE) -f $(YAML) kill

dops:
	$(COMPOSE) -f $(YAML) ps

dorm:
	$(COMPOSE) -f $(YAML) rm --force
