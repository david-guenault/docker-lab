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


cleanall:
	rm -Rf CA server client

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
	rm -f *.csr *.cnf

localserverconfig:
	cp /etc/default/docker /etc/default/docker.$$(date +%s)
	mkdir -p /etc/pki/docker
	rm -Rf /etc/pki/docker
	cp -a server/$(SERVER) /etc/pki/docker
	sed -i "/^DOCKER_OPTS/d" /etc/default/docker
	echo "DOCKER_OPTS=\"-H tcp://0.0.0.0:$(DOCKERPORT) --tlsverify --tlscacert=/etc/pki/docker/ca.pem --tlscert=/etc/pki/docker/server-cert.pem --tlskey=/etc/pki/docker/server-key.pem --label storage=$(SERVER)\"" >> /etc/default/docker
	service docker restart

localclientconfig:
	rm -Rf ~/.docker
	mkdir -pv ~/.docker
	cp -v client/$(CLIENT)/ca.pem ~/.docker/
	cp -v client/$(CLIENT)/cert.pem ~/.docker/
	cp -v client/$(CLIENT)/key.pem ~/.docker/
	sed -i "/^DOCKER_/d" ~/.bashrc
	echo "export DOCKER_TLS_VERIFY=1" >> ~/.bashrc
	echo "export DOCKER_HOST=tcp://$(SERVER):$(DOCKERPORT)" >> ~/.bashrc

serverconfig:
	@-echo "1 - Put the server/$(SERVER) folder on the target docker host (with scp for example"
	@-echo "2 - Logon your target host (as root if you don't have sudo) : $(SERVER) and go into the $(SERVER) folder"
	@-echo "3 - Issue the following commands"
	@-echo "     mkdir -p /etc/pki/docker"
	@-echo "     cp * /etc/pki/docker"
	@-echo "     sed -i "/^DOCKER_OPTS/d" /etc/default/docker"
	@-echo "     echo "DOCKER_OPTS=\"-H tcp://0.0.0.0:$(DOCKERPORT) --tlsverify --tlscacert=/etc/pki/docker/ca.pem --tlscert=/etc/pki/docker/server-cert.pem --tlskey=/etc/pki/docker/server-key.pem --label storage=$(SERVER)\"" >> /etc/default/docker"
	@-echo "     service docker restart"

clientconfig:
	@-echo "1 - Put the client/$(CLIENT) folder on the target docker host (with scp for example)"
	@-echo "2 - Logon your target host (as the user that will use dockerclient) : $(CLIENT) and go into the $(CLIENT) folder"
	@-echo "3 - Issue the following commands"
	@-echo "     mkdir -p ~/.docker"
	@-echo "     cp -v *.pem ~/.docker"
	@-echo "     sed -i "/^DOCKER_/d" ~/.bashrc"
	@-echo "     echo \"export DOCKER_TLS_VERIFY=1\" >> ~/.bashrc"
	@-echo "     echo "export DOCKER_HOST=tcp://$(SERVER):$(DOCKERPORT)" >> ~/.bashrc"
	@-echo "     source ~/.bashrc"

startserver:
	$(SUDO) $(DOCKER) -d -D --tlsverify --tlscacert=$$(pwd)/CA/ca.pem --tlscert=$$(pwd)/server/$(SERVER)/server-cert.pem --tlskey=$$(pwd)/server/$(SERVER)/server-key.pem -H=0.0.0.0:$(DOCKERPORT)

dockerverify:
	$(DOCKER) --tlscacert=CA/ca.pem --tlscert=client/$(CLIENT)/cert.pem --tlskey=client/$(CLIENT)/key.pem --tlsverify  -H $(DOCKERHOST):$(DOCKERPORT) version

curlverify:
	$(CURL) --cert client/$(CLIENT)/cert.pem --key client/$(CLIENT)/key.pem --cacert CA/ca.pem https://$(SERVER):$(DOCKERPORT)/images/json

permission:
	chmod -v 0400 CA/ca-key.pem client/$(CLIENT)/key.pem server/$(SERVER)/server-key.pem
	chmod -v 0444 CA/ca.pem server/$(SERVER)/server-cert.pem client/$(CLIENT)/cert.pem

.PHONY: ca cleanall client clientconfig curlverify dockerverify localclientconfig localserverconfig permission server serverconfig startserver



