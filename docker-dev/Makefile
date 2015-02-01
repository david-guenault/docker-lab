TAG=master

clone:
	git clone https://github.com/docker/docker

checkout:
	if [ "$(TAG)" != "master" ]; then cd docker && git checkout tags/$(TAG); fi

pull:
	cd docker && git pull

build: 
	cd docker && \
	make build && \
	make binary

rebuild: clean clone checkout build

clean:
	rm -Rf docker

backupdocker:
	@-if [ -z "$$(which docker.orig)" ]; then \
		DOCKERBIN=$$(which docker); \
		cp -a $$DOCKERBIN $$DOCKERBIN.orig; \
		echo "Backup done"; \
	else \
		echo "Backup already exist"; \
	fi

switch2dev:
	VERSION=$$(cat docker/VERSION); \
	service docker stop; \
	cp  docker/bundles/$$VERSION/binary/docker $$(which docker); \
	service docker start

switch2stable:
	service docker stop; \
	cp  $$(which docker).orig $$(which docker); \
	service docker start
