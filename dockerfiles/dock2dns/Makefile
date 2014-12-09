NAME = dock2dns
RUNNAME = dock2dns
TAG = latest

include ../common/Makefile

test:
	$(DOCKER) run --rm -v /var/run/docker.sock:/docker.sock --name $(RUNNAME) $(IMAGE) --domain=dock2dns.lan --socket=unix://docker.sock --etcd="http://172.17.42.1:4001"
