COMPOSEFILE=ske.yml
DOCKER=/usr/bin/docker
COMPOSE=/usr/local/bin/docker-compose

build: clean
	cd ../dockerfiles/shinken-enterprise-2.0.3-update/ && \
	$(MAKE) build 

ips:
	@-for c in $$($(COMPOSE) -f $(COMPOSEFILE) ps 2>/dev/null | awk '{print $$1}' | tail -n $$(docker-compose -f $(COMPOSEFILE) ps -q 2> /dev/null | wc -l)); do IP=$$($(DOCKER) inspect -f '{{.NetworkSettings.IPAddress}}' $$c); echo "$$c => $$IP"; done

up:
	$(COMPOSE) -f $(COMPOSEFILE) up -d

start:
	$(COMPOSE) -f $(COMPOSEFILE) start

stop:
	$(COMPOSE) -f $(COMPOSEFILE) stop

restart:
	$(COMPOSE) -f $(COMPOSEFILE) restart

ps:
	$(COMPOSE) -f $(COMPOSEFILE) ps

clean:
	@-$(COMPOSE) -f $(COMPOSEFILE) kill
	@-$(COMPOSE) -f $(COMPOSEFILE) rm --force

