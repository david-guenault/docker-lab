DOCKER=/usr/bin/docker
COMPOSE=/usr/local/bin/docker-compose
YAML=ha.yml
IMAGE=dguenault/shinken-base:2.2

extractconfig:
	$(DOCKER) run -d --name tempsk22 $(IMAGE) top && \
	$(DOCKER) cp tempsk22:/etc/shinken . && \
	$(DOCKER) stop tempsk22 && \
	$(DOCKER) rm tempsk22

up:
	$(COMPOSE) -f $(YAML) up -d

start:
	$(COMPOSE) -f $(YAML) start

stop:
	$(COMPOSE) -f $(YAML) stop

ps: 	
	$(COMPOSE) -f $(YAML) ps

rm:
	$(COMPOSE) -f $(YAML) rm --force
