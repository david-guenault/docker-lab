NAME = skydnsbuild
RUNNAME = skydnsbuild
TAG = latest

include ../../common/Makefile

bin: build
	$(DOCKER) create -ti --name $(RUNNAME) $(IMAGE) tail -f 
	$(DOCKER) cp $(RUNNAME):/gocode/bin/skydns ../files/
	$(MAKE) clean
	$(MAKE) rm
	
