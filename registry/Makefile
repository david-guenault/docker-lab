DOCKER=/usr/bin/docker
DOCKER_COMPOSE=/usr/local/bin/docker-compose
HTPASSWD=/usr/bin/htpasswd
CONFIG=config.yml
FLAVOR=local
HOST=node3

init: htpasswd getcerts

htpasswd:
	$(HTPASSWD) -c -b ./registry.htpasswd $(USER) $(PASSWORD)

getcerts:
	cp ../docker-pki/ca/ca-chain.crt .
	cp ../docker-pki/bundles/nginx-$(HOST)/cert.pem .
	cp ../docker-pki/bundles/nginx-$(HOST)/key.pem .

run:
	export EXTERNAL_IP_ADDR=$$(ping -c 1 $$(hostname -s) | head -n 2 | tail -n 1 | sed -re "s/.*\(([^\)]+).*$$/\1/g") && \
	$(DOCKER_COMPOSE) -f registry.yml up

start:
	@-$(DOCKER_COMPOSE) -f registry.yml start

stop:
	@-$(DOCKER_COMPOSE) -f registry.yml stop 

kill:
	@-$(DOCKER_COMPOSE) -f registry.yml kill 

restart: stop start

rm: stop
	@-$(DOCKER_COMPOSE) -f registry.yml rm --force 

clean: rm
	rm -f *.pem *.htpasswd
