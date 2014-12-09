NAMESPACE = dguenault
NAME = elk
RUNNAME = elk 
TAG = latest
BROWSER = /usr/bin/google-chrome

clean: containerclean imageclean

imageclean:
	- docker rmi $(NAMESPACE)/$(NAME):$(TAG)
	- docker rmi $$(docker images |grep "none" |awk '{print $3'})

containerclean:
	- docker stop $(RUNNAME)
	- docker rm $(RUNNAME)

build: 
	docker build --force-rm -t $(NAMESPACE)/$(NAME):$(TAG) .

run:
	JOB=$$(docker run -v /etc/localtime:/etc/localtime:ro --name $(RUNNAME) $(NAMESPACE)/$(NAME):$(TAG) > /dev/null 2>&1 &)

interactive:
	docker run -ti --rm -v /etc/localtime:/etc/localtime:ro --name $(RUNNAME) $(NAMESPACE)/$(NAME):$(TAG) /bin/bash

start:
	docker start $(RUNNAME)

stop:
	docker stop $(RUNNAME)

supervisor:
	$(BROWSER) http://$$(docker inspect --format='{{.NetworkSettings.IPAddress}}' $(RUNNAME)):9001
	
kibana:
	$(BROWSER) http://$$(docker inspect --format='{{.NetworkSettings.IPAddress}}' $(RUNNAME))/kibana

elastichq:
	$(BROWSER) http://$$(docker inspect --format='{{.NetworkSettings.IPAddress}}' $(RUNNAME)):9200/_plugin/HQ

enter:
	sudo ./go.sh $(RUNNAME)

ip:
	docker inspect --format='{{.NetworkSettings.IPAddress}}' $(RUNNAME)
