IMAGES= centos-ssh shinken shinken-arbiter shinken-poller shinken-receiver shinken-reactionner shinken-broker shinken-scheduler skydock thruk dock2dns
DOCKER=/usr/bin/docker
MAKE=/usr/bin/make

build:
ifdef IMG
	cd $$IMG && $(MAKE) build 
else
	for image in $(IMAGES); do \
		cd $$image && $(MAKE) build && cd .. ; \
	done
endif


clean:
	for image in $(IMAGES); do \
		cd $$image && $(MAKE) clean && cd .. ; \
	done

.PHONY: build clean
