REPOSITORY=dguenault
NAME = dock2dns
RUNNAME = dock2dns
TAG = latest

DOCKER=/usr/bin/docker
COMPOSE=/usr/local/bin/docker-compose
YAML=$(NAME).yml

build:
	$(DOCKER) build -t $(REPOSITORY)/$(NAME):$(TAG) .

up:
	$(COMPOSE) -f $(YAML)  up -d

start:
	$(COMPOSE) -f $(YAML) start

stop:
	$(COMPOSE) -f $(YAML) stop

kill:
	$(COMPOSE) -f $(YAML) kill

ps:
	$(COMPOSE) -f $(YAML) ps

rm:
	$(COMPOSE) -f $(YAML) rm --force
