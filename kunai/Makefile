IMAGES=kunai

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