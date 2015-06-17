DOCKER=/usr/bin/docker
COMPOSE=/usr/local/bin/docker-compose
YAML=ha.yml
IMAGE=dguenault/shinken-base:2.2
CONFIG=shinken

help:
	echo "make extractconfig get original shinken configuration folder from base image"
	echo "ex: make extractconfig CONFIG=[target folder name for extracted shinken config folder]"
	echo ""

	echo "make up: used for a first start (aka project does not exist and have never been runed"
	echo "make stop: gracefuly stop the project"
	echo "make kill: kill the project without waiting for application to be down"
	echo "make start: start an already existing project"
	echo "make ps: display states of the project containers"
	echo "make rm: remove project containers"
	echo ""

	echo "make fixuser: if you plan to use the thruk config tool, docker need to map exisiting user in thruk container."
	echo "ex :make fixuser USR=www-data CONTAINER=thruk FOLDER=/etc/shinken"
	echo ""

	echo "configuration default to ha.yml. You can specify another shinken project setup by using the YAML parameter in each target"
	echo ""
	echo "exemple:"
	echo "make up YAML=single.yml"
	echo "make extractconfig CONFIG=shinken-simple"
	echo "make fixuser USR=www-data CONTAINER=thruk FOLDER=/etc/shinken YAML=single.yml"



extractconfig: 
	$(DOCKER) run -d --name tempsk22 $(IMAGE) top && \
	rm -Rf /tmp/$(CONFIG) && \
	$(DOCKER) cp tempsk22:/etc/shinken /tmp && \
	cp -a /tmp/shinken ./$(CONFIG) && \
	$(DOCKER) stop tempsk22 && \
	$(DOCKER) rm tempsk22

up:
	$(COMPOSE) -f $(YAML) up -d

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

# fix user rights for config
fixuser:
	@if [ -z "$(USR)" ] || [ -z "$(CONTAINER)" ] || [ -z "$(FOLDER)" ];then \
		echo "you must specify :"; \
		echo " - the user to be created in container (USR)"; \
		echo " - the container to apply the fix to (CONTAINER)"; \
		echo " - the folder on which to apply the rights (FOLDER)"; \
		exit 2; \
	fi; \
	FOLDER=/etc/shinken; \
	REALCONTAINER=$$($(COMPOSE) -f $(YAML) ps $$CONTAINER 2>/dev/null | tail -n 1 | awk '{print $$1}'); \
	exist=$$($(DOCKER) exec $$REALCONTAINER cat /etc/passwd 2>/dev/null | grep $(USR)); \
	UID=$$(cat /etc/passwd | grep $(USER) | awk -F: '{print $$3}'); \
	GID=$$(cat /etc/passwd | grep $(USER) | awk -F: '{print $$4}'); \
	GROUP=$$(cat /etc/group | grep -E "\w+:\w:$$GID" | awk -F: '{print $$1}'); \
	if [ -z "$$exists"]; then \
		echo "Create group $$GROUP with group id $$GID"; \
		$(DOCKER) exec $$REALCONTAINER groupadd -g $$GID $$GROUP; \
		echo "Create user $(USER) with group id $$GID and user id $$UID"; \
		$(DOCKER) exec $$REALCONTAINER useradd -u $$UID -g $$GID $$GROUP; \
	fi; \
	echo "Owner :"; \
	echo " - USER NAME : $(USER)"; \
	echo " - UID : $$UID"; \
	echo " - GROUP NAME : $$GROUP"; \
	echo " - GID : $$GID"; \
	echo ""; \
	echo "Applying fix on $(FOLDER) in container $(CONTAINER) ($$REALCONTAINER)"; \
	echo " - Change owner of folder $(FOLDER) to user $(USER) with group $$GROUP"; \
	$(DOCKER) exec $$REALCONTAINER chown -R $(USER):$$GROUP $(FOLDER); \
	echo " - Add read/write right to group $$GROUP on folder $(FOLDER)"; \
	$(DOCKER) exec $$REALCONTAINER chmod -R g+rw $(FOLDER); \
	echo " - Add user $(USR) to secondary group $$GROUP (gid:$$GID)"; \
	$(DOCKER) exec $$REALCONTAINER usermod -a -G $$GROUP $(USR); \



