# certs data
COUNTRY=FR
STATE=Languedoc Roussillon
LOCALITY=Perpignan
ORGANIZATION=BOX4PROD
DAYS=3650
SIZE=2048

# certs CN
HOST=$$(hostname -s)
SERVER=$(HOST)
CLIENT=$(HOST)

# Docker
DOCKERHOST=$(HOST)
DOCKERPORT=2375

# Binaries
DOCKER=/usr/bin/docker
IPTABLES=/sbin/iptables
OPENSSL=/usr/bin/openssl
CURL=/usr/bin/curl
SUDO=/usr/bin/sudo

define SETUPSCRIPT=
#!/bin/bash  
mkdir -p /etc/pki/docker 
cp ./*.pem /etc/pki/docker 
sed -i "/^DOCKER_OPTS/d" /etc/default/docker 
echo "DOCKER_OPTS=\"-H tcp://0.0.0.0:$(DOCKERPORT) --tlsverify --tlscacert=/etc/pki/docker/ca.pem --tlscert=/etc/pki/docker/server-cert.pem --tlskey=/etc/pki/docker/server-key.pem --label storage=$(SERVER)\" >> /etc/default/docker 
service docker restart 
endef



ca:
	mkdir CA && \
	cd CA && \
	echo 01 > crl && \
	echo 01 > serial && \
	touch index && \
	$(OPENSSL) req -new \
	-newkey rsa:$(SIZE) \
	-days $(DAYS) \
	-nodes -x509 \
	-subj "/C=$(COUNTRY)/ST=$(STATE)/L=$(LOCALITY)/O=$(ORGANIZATION)/CN=$(HOST)" \
	-keyout ca-key.pem \
	-out ca.pem

server: 
	mkdir -p server/$(SERVER) && \
	cd server/$(SERVER) && \
	$(OPENSSL) genrsa -out server-key.pem $(SIZE) && \
	$(OPENSSL) req -subj "/CN=$(SERVER)" -new -key server-key.pem -out server.csr && \
	$(OPENSSL) x509 -req -days $(DAYS) -in server.csr -CA ../../CA/ca.pem -CAkey ../../CA/ca-key.pem -CAcreateserial -out server-cert.pem  && \
	rm -f server.csr .srl && \
	cp ../../CA/ca.pem ./ && \
	cp ../../templates/serversetup.template ./setup.sh && \
	sed -i "s/@PORT@/$(DOCKERPORT)/g" setup.sh && \
	sed -i "s/@SERVER@/$(SERVER)/g" setup.sh && \
	chmod +x setup.sh


client: 
	mkdir -p client/$(CLIENT) && \
	cd client/$(CLIENT) && \
	$(OPENSSL) genrsa -out key.pem $(SIZE) && \
	$(OPENSSL) req -subj '/CN=client' -new -key key.pem -out client.csr && \
	echo extendedKeyUsage = clientAuth > extfile.cnf && \
	$(OPENSSL) x509 -req -days $(DAYS) -in client.csr -CA ../../CA/ca.pem -CAkey ../../CA/ca-key.pem -CAcreateserial -out cert.pem -extfile extfile.cnf && \
	cp ../../CA/ca.pem . && \
	rm -f *.csr *.cnf && \
	cp ../../templates/clientsetup.template ./setup.sh && \
	sed -i "s/@PORT@/$(DOCKERPORT)/g" setup.sh && \
	sed -i "s/@SERVER@/$(CLIENT)/g" setup.sh && \
	chmod +x setup.sh

cleanall:
	rm -Rf CA server client

.PHONY: cleanall ca server client



