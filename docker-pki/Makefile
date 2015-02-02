# certs data
COUNTRY=FR
STATE=Languedoc Roussillon
LOCALITY=Perpignan
ORGANIZATION=BOX4PROD
DAYS=3650
SIZE=2048
# certs default
HOST=$$(hostname -s)
TYPE=daemon
# Docker
DOCKERHOST=$(HOST)
DOCKERPORT=2375
# Binaries
DOCKER=/usr/bin/docker
SWARM=/usr/bin/swarm
OPENSSL=/usr/bin/openssl

ca:
	mkdir -p CA && \
	BASE=$$(readlink -f .) && \
	IP=$$(ping -c 1 $(HOST) | head -n 1 | awk '{print $$3}' | sed -e "s/(//g" -e "s/)//g") && \
	cp templates/openssl.cnf CA/ssl.cnf && \
	cd CA && \
	sed -i \
		 -e "s/@COUNTRY@/$(COUNTRY)/g" \
		 -e "s/@STATE@/$(STATE)/g" \
		 -e "s/@LOCALITY@/$(LOCALITY)/g" \
		 -e "s/@ORGANIZATION@/$(ORGANIZATION)/g"  \
		 -e "s/@CN@/$(HOST)/g" \
		 -e "s/@CAPATH@/CA/g" ssl.cnf && \
	touch password && \
	chmod 600 password && \
	cat /dev/urandom | head -c 128 | base64 | sed -n '{p;p;}' >> password && \
	$(OPENSSL) genrsa \
		-des3 \
		-passout file:password \
		-out cakey.pem 2048 && \
	$(OPENSSL) req \
		-new \
		-x509 \
		-days $(DAYS) \
		-batch \
		-passin file:password \
		-key cakey.pem \
		-passout file:password \
		-out ca.pem

cert: 
	if [ -f "ca.srl" ]; then \
		SOPT=$(SERIALOPT); \
	else \
		SOPT=$(SERIALOPTNEW); \
	fi && \
	mkdir -p CA/certs/$(TYPE)-$(HOST) && \
	cd CA/certs/$(TYPE)-$(HOST) && \
	IP=$$(ping -c 1 $(HOST) | head -n 1 | awk '{print $$3}' | sed -e "s/(//g" -e "s/)//g") && \
	cp ../../ssl.cnf ssl.cnf && \
	sed -i "s/req_extensions = .*$$/req_extensions = $(TYPE)/g" ssl.cnf && \
	echo "IP.1 = $$IP" >> ssl.cnf && \
	$(OPENSSL) genrsa \
		-des3 \
		-passout file:../../password \
		-out key.pem $(SIZE) && \
	$(OPENSSL) req  -subj "/CN=$(HOST)" -new \
		-batch \
		-passin file:../../password \
		-key key.pem \
		-passout file:../../password \
		-out req.csr -config ssl.cnf && \
	$(OPENSSL) x509 -req -days $(DAYS) \
		-passin file:../../password \
		-in req.csr \
		-CA ../../ca.pem \
		-CAkey ../../cakey.pem \
		-CAserial ../../ca.srl \
		-CAcreateserial \
		-extfile ssl.cnf \
		-extensions $(TYPE) \
		-out cert.pem && \
	$(OPENSSL) rsa \
		-passin file:../../password \
		-in key.pem \
		-out key.pem \

testserver:
	$(DOCKER) -d -D -H tcp://0.0.0.0:$(DOCKERPORT) --tlsverify --tlscacert=CA/ca.pem --tlscert=CA/certs/daemon-$(HOST)/cert.pem --tlskey=CA/certs/daemon-$(HOST)/key.pem --label storage=$(HOST)

testclient:
	$(DOCKER) -H tcp://$(HOST):$(DOCKERPORT) --tlsverify --tlscacert=CA/ca.pem --tlscert=CA/certs/client-$(HOST)/cert.pem --tlskey=CA/certs/client-$(HOST)/key.pem version
	
reset:
	@-service docker stop
	rm -Rf /etc/pki/docker ~/.docker/*.pem
	sed -i "/^DOCKER_OPTS/d" /etc/default/docker 
	echo DOCKER_OPTS=\"-H unix:///var/run/docker.sock\" >> /etc/default/docker
	sed -i "/^export DOCKER/d" ~/.bashrc
	@-service docker start

setup:
	@-service docker stop
	mkdir -p /etc/pki/docker
	cp CA/certs/server-$(HOST)/*.pem /etc/pki/docker/
	cp CA/ca.pem /etc/pki/docker
	sed -i  "/^DOCKER_OPTS=/d" /etc/default/docker
	echo DOCKER_OPTS=\"-H tcp://0.0.0.0:$(DOCKERPORT) --tlsverify --tlscacert=/etc/pki/docker/ca.pem --tlscert=/etc/pki/docker/cert.pem --tlskey=/etc/pki/docker/key.pem --label storage=$(HOST)\" >> /etc/default/docker
	@-service docker start
	cp CA/certs/client-$(HOST)/*.pem ~/.docker/
	cp CA/ca.pem ~/.docker/
	echo "export DOCKER_TLS_VERIFY=1" >> ~/.bashrc
	echo "export DOCKER_HOST=tcp://$(HOST):$(DOCKERPORT)" >> ~/.bashrc




# officialserver:
# 	$(DOCKER) -d -D -H tcp://0.0.0.0:$(DOCKERPORT) --tlsverify --tlscacert=CA/ca.pem --tlscert=CA/server.pem --tlskey=CA/serverkey.pem --label storage=$(HOST)

# officialclient:
# 	$(DOCKER) -H tcp://node1:$(DOCKERPORT) --tlsverify --tlscacert=CA/ca.pem --tlscert=CA/client.pem --tlskey=CA/clientkey.pem version

# official: 
# 	mkdir -p CA && \
# 	rm -f *.pem *.csr *.key *.txt
# 	BASE=$$(readlink -f .) && \
# 	IP=$$(ping -c 1 $(HOST) | head -n 1 | awk '{print $$3}' | sed -e "s/(//g" -e "s/)//g") && \
# 	cp templates/openssl.cnf CA/ssl.cnf && \
# 	cd CA && \
# 	sed -i \
# 		 -e "s/@COUNTRY@/$(COUNTRY)/g" \
# 		 -e "s/@STATE@/$(STATE)/g" \
# 		 -e "s/@LOCALITY@/$(LOCALITY)/g" \
# 		 -e "s/@ORGANIZATION@/$(ORGANIZATION)/g"  \
# 		 -e "s/@CN@/$(HOST)/g" \
# 		 -e "s/@DNS@/$(HOST)/g" \
# 		 -e "s/@IP@/$$IP/g" \
# 		 -e "s/@CAPATH@/CA/g" ssl.cnf && \
# 	openssl genrsa -out cakey.pem 2048  &&\
# 	openssl req -new -subj "/CN=node1" -x509 -days 365 -key cakey.pem -sha256 -out ca.pem && \
# 	openssl genrsa -out serverkey.pem 2048 && \
# 	openssl req -subj "/CN=node1" -new -key serverkey.pem -out server.csr && \
# 	openssl x509 -req -days 365 -in server.csr -CA ca.pem -CAkey cakey.pem -CAcreateserial -out server.pem && \
# 	openssl genrsa -out clientkey.pem 2048 && \
# 	openssl req -subj "/CN=client" -new -key clientkey.pem -out client.csr && \
# 	echo "extendedKeyUsage = clientAuth" > ext.cnf && \
# 	openssl x509 -req -days 365 -in client.csr -CA ca.pem -CAkey cakey.pem -CAcreateserial -out client.pem -extfile ext.cnf && \
# 	echo

clean:
	rm -Rf CA

.PHONY: ca cleanall  cert reset



