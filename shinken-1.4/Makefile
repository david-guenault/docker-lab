IMAGES=shinken-1.4 shinken-arbiter-1.4 shinken-poller-1.4 shinken-receiver-1.4 shinken-reactionner-1.4 shinken-scheduler-1.4 shinken-broker-1.4

clean:
	$(MAKE) loop ACTION=clean BASE=$$(pwd)

build: 
	$(MAKE) loop ACTION=build BASE=$$(pwd)

push:
	$(MAKE) loop ACTION=push BASE=$$(pwd)

loop:
	for IMG in $(IMAGES); \
	do \
		cd $(BASE)/../dockerfiles/$$IMG; \
		$(MAKE) $(ACTION); \
	done;

.PHONY: clean build push loop