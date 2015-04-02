REGISTRYNAME=registry
REGISTRYHOSTNAME=registry
REGISTRYPORT=5000
NGINXHOSTNAME=node3
NGINXNAME=nginx
NGINXPORT=8080
NGINXIP=$(NGINXHOSTNAME)

DOCKER=/usr/bin/docker
DOCKER_COMPOSE=/usr/local/bin/docker-compose
HTPASSWD=/usr/bin/htpasswd

USER=dguenault
PASSWORD=dfgdfg

void:

init: htpasswd getcerts configure

configure:
	@if [ -z "$(HOST)" ]; then \
		echo "HOST is required"; \
		exit 2; \
	fi;
	@if [ -z "$(PORT)" ]; then \
		echo "PORT is required"; \
		exit 2; \
	fi;
	@cp docker-registry.conf.template docker-registry.conf
	@cp registry.yml.template registry.yml
	@IP=$$(ping -c 1 $(HOST) | head -n 2 | tail -n 1 | sed -re "s/.*\(([^\)]+).*$$/\1/g") && \
	sed -i "s/@REGISTRYNAME@/$(REGISTRYNAME)/g" docker-registry.conf && \
	sed -i "s/@REGISTRYHOSTNAME@/$(REGISTRYHOSTNAME)/g" docker-registry.conf && \
	sed -i "s/@@/$()/g" docker-registry.conf && \
	sed -i "s/@@/$()/g" docker-registry.conf && \
	
	sed -i "s/@HOST@/$(HOST)/g" registry.yml && \

htpasswd:
	@if [ -z "$(USER)" ]; then \
		echo "USER is required"; \
		exit 2; \
	fi;
	@if [ -z "$(PASSWORD)" ]; then \
		echo "PASSWORD is required"; \
		exit 2; \
	fi;
	@-$(HTPASSWD) -c -b ./registry.htpasswd $(USER) $(PASSWORD)

getcerts:
	@cp ../docker-pki/bundles/nginx-$(HOST)/cert.pem .
	@cp ../docker-pki/bundles/nginx-$(HOST)/key.pem .

# control
run:
	@if [ -z "$(HOST)" ]; then \
		echo "HOST is required"; \
		exit 2; \
	fi;
	$(DOCKER_COMPOSE) -f registry.yml up -d


kill:
	@-$(DOCKER_COMPOSE) -f registry.yml kill 

restart: stop start

start:
	@-$(DOCKER_COMPOSE) -f registry.yml start

stop:
	@-$(DOCKER_COMPOSE) -f registry.yml stop 

# clean up
clean: 
	@-rm -f *.pem *.htpasswd *.key *.crt
	@-rm registry.yml docker-registry.conf

rm:
	@-$(DOCKER_COMPOSE) -f registry.yml rm --force 

.PHONY: clean cleanconf configure getcerts htpasswd init kill restart rm run start stop void