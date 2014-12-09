# dock2dns service discovery 
# VERSION	latest	

FROM     	dguenault/centos-ssh:6
MAINTAINER	David GUENAULT

# install docker python api
RUN	pip install docker-py 

# add dock2dns
ADD 	files/dock2dns.py /dock2dns.py
RUN	chmod +x /dock2dns.py

ENTRYPOINT ["/dock2dns.py"]
