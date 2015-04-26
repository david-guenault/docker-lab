# dock2dns service discovery 
# VERSION	latest	
FROM              python:onbuild
MAINTAINER	David GUENAULT

ENV     ETCD http://etcd:4001
ENV     DOCKER https://node3:2375
ENV     DOMAIN box4prod.lan

COPY    requirements.txt /requirements.txt

# prerequisites
RUN     apt-get update && \
            apt-get -y install vim-nox python-dev gcc openssl libssl-dev python-pip&& \
            pip install --upgrade pip && \
            pip install -r /requirements.txt && \
            mkdir /certs

# add dock2dns
COPY 	dock2dns.py /dock2dns.py
COPY    certs/ca.pem /certs/
COPY    certs/cert.pem /certs/
COPY    certs/key.pem /certs/

RUN	chmod +x /dock2dns.py

CMD /dock2dns.py --tls --ca=/certs/ca.pem --cert=/certs/cert.pem --key=/certs/key.pem --domain=$DOMAIN --etcd=$ETCD --socket=$DOCKER
