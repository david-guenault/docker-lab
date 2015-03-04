ORGANIZATION=BOX4PROD
DOMAIN=box4prod
TLD=com
UNIT=IT
DAYS=3650
SIZE=2048
OPENSSL=/usr/bin/openssl
DOCKER=/usr/bin/docker
PKI=/etc/pki/docker
CRLHOST=node3
CRLPORT=8080
CRLURI=http://$(CRLHOST):$(CRLPORT)/signing-ca.crl
CRLCONTAINER=$(ORGANIZATION)crl

caconfig:
	mkdir -p etc
	cp templates/root-ca.conf.template etc/root-ca.conf
	cp templates/signing-ca.conf.template etc/signing-ca.conf
	sed -i \
		-e "s/@DOMAIN@/$(DOMAIN)/g" \
		-e "s/@TLD@/$(TLD)/g" \
		-e "s/@ORGANIZATION@/$(ORGANIZATION)/g" \
		-e "s/@SIZE@/$(SIZE)/g" \
		-e "s/@DAYS@/$(DAYS)/g" \
		-e "s#@CRLURI@#$(CRLURI)#g" \
		etc/root-ca.conf
	sed -i \
		-e "s/@DOMAIN@/$(DOMAIN)/g" \
		-e "s/@TLD@/$(TLD)/g" \
		-e "s/@ORGANIZATION@/$(ORGANIZATION)/g" \
		-e "s/@SIZE@/$(SIZE)/g" \
		-e "s/@DAYS@/$(DAYS)/g" \
		-e "s#@CRLURI@#$(CRLURI)#g" \
		etc/signing-ca.conf

serverconfig:
	cp templates/server.conf.template etc/server-$(HOST).conf
	sed -i \
		-e "s/@DOMAIN@/$(DOMAIN)/g" \
		-e "s/@ORGANIZATION@/$(ORGANIZATION)/g" \
		-e "s/@TLD@/$(TLD)/g" \
		-e "s/@UNIT@/$(UNIT)/g" \
		-e "s/@SIZE@/$(SIZE)/g" \
		-e "s/@CN@/$(HOST)/g" \
		-e "s/@HOST@/$(HOST)/g" \
		-e "s#@CRLURI@#$(CRLURI)#g" \
		etc/server-$(HOST).conf

clientconfig:
	cp templates/client.conf.template etc/client-$(HOST).conf
	sed -i \
		-e "s/@DOMAIN@/$(DOMAIN)/g" \
		-e "s/@ORGANIZATION@/$(ORGANIZATION)/g" \
		-e "s/@TLD@/$(TLD)/g" \
		-e "s/@UNIT@/$(UNIT)/g" \
		-e "s/@SIZE@/$(SIZE)/g" \
		-e "s/@CN@/$(HOST)/g" \
		-e "s/@HOST@/$(HOST)/g" \
		-e "s#@CRLURI@#$(CRLURI)#g" \
		etc/client-$(HOST).conf

ca: caconfig
	mkdir -p ca/root-ca/private ca/root-ca/db crl certs && \
	chmod 700 ca/root-ca/private && \
	cp /dev/null ca/root-ca/db/root-ca.db && \
	cp /dev/null ca/root-ca/db/root-ca.db.attr && \
	echo 01 > ca/root-ca/db/root-ca.crt.srl && \
	echo 01 > ca/root-ca/db/root-ca.crl.srl && \
	$(OPENSSL) req -new \
    		-config etc/root-ca.conf \
    		-out ca/root-ca.csr \
    		-keyout ca/root-ca/private/root-ca.key \
    		-nodes \
    		-batch && \
	$(OPENSSL) ca -selfsign \
    		-config etc/root-ca.conf \
    		-in ca/root-ca.csr \
    		-out ca/root-ca.crt \
    		-batch \
    		-extensions root_ca_ext && \
	mkdir -p ca/signing-ca/private ca/signing-ca/db crl certs && \
	chmod 700 ca/signing-ca/private && \
	cp /dev/null ca/signing-ca/db/signing-ca.db && \
	cp /dev/null ca/signing-ca/db/signing-ca.db.attr && \
	echo 01 > ca/signing-ca/db/signing-ca.crt.srl && \
	echo 01 > ca/signing-ca/db/signing-ca.crl.srl && \
	$(OPENSSL) req -new \
    		-config etc/signing-ca.conf \
    		-out ca/signing-ca.csr \
    		-nodes \
    		-batch \
    		-keyout ca/signing-ca/private/signing-ca.key && \
	$(OPENSSL) ca \
		-config etc/root-ca.conf \
    		-in ca/signing-ca.csr \
    		-out ca/signing-ca.crt \
    		-extensions signing_ca_ext \
    		-batch && \
    	cat ca/signing-ca.crt ca/root-ca.crt > ca/ca-chain.crt

crl:
	$(OPENSSL) ca -gencrl \
    		-config etc/signing-ca.conf \
    		-out crl/signing-ca.crl && \
    	$(MAKE) crlimage && \
    	$(MAKE) startcrlendpoint 

revokecert:
	$(OPENSSL) ca \
		-keyfile ca/signing-ca/private/signing-ca.key \
		-cert ca/signing-ca.crt \
		-revoke certs/$(TYPE)-$(HOST).crt \
		-config etc/signing-ca.conf && \
	$(MAKE) crl
	
crlimage:
	$(DOCKER) build -t $$(echo $(ORGANIZATION) | tr '[:upper:]' '[:lower:]')crl .

startcrlendpoint: stopcrlendpoint removecrlendpoint
	$(DOCKER) run -d --name $$(echo $(CRLCONTAINER) | tr '[:upper:]' '[:lower:]') -p $(CRLPORT):80 $$(echo $(CRLCONTAINER) | tr '[:upper:]' '[:lower:]'):latest

stopcrlendpoint:
	@-$(DOCKER) stop $$(echo $(CRLCONTAINER) | tr '[:upper:]' '[:lower:]')

removecrlendpoint:
	@-$(DOCKER) rm $$(echo $(CRLCONTAINER) | tr '[:upper:]' '[:lower:]')

servercert: serverconfig
	SAN="DNS:$(HOST)" \
	$(OPENSSL) req \
		-new -config etc/server-$(HOST).conf \
		-out certs/server-$(HOST).csr \
		-keyout certs/server-$(HOST).key \
		-nodes \
		-batch && \
	$(OPENSSL) ca \
		-config etc/signing-ca.conf \
		-in certs/server-$(HOST).csr \
		-out certs/server-$(HOST).crt \
		-extensions server_ext \
		-batch
	$(OPENSSL) pkcs12 -export \
    		-name "$(HOST)" \
    		-inkey certs/server-$(HOST).key \
    		-in certs/server-$(HOST).crt \
    		-out certs/server-$(HOST).p12 \
    		-password pass: \
    		-nodes

clientcert: clientconfig
	SAN="DNS:$(HOST)" \
	$(OPENSSL) req \
		-new -config etc/client-$(HOST).conf \
		-out certs/client-$(HOST).csr \
		-keyout certs/client-$(HOST).key \
		-nodes \
		-batch && \
	$(OPENSSL) ca \
		-config etc/signing-ca.conf \
		-in certs/client-$(HOST).csr \
		-out certs/client-$(HOST).crt \
		-extensions client_ext \
		-batch
	$(OPENSSL) pkcs12 -export \
    		-name "$(HOST)" \
    		-inkey certs/client-$(HOST).key \
    		-in certs/client-$(HOST).crt \
    		-out certs/client-$(HOST).p12 \
    		-password pass: \
    		-nodes


dockerserverbundle:
	rm -Rf bundles/server-$(HOST)
	mkdir -p bundles/server-$(HOST)
	cp certs/server-$(HOST).crt bundles/server-$(HOST)/cert.pem
	cp certs/server-$(HOST).key bundles/server-$(HOST)/key.pem
	cp ca/ca-chain.crt bundles/server-$(HOST)/ca.pem
	echo "#! /bin/bash" > bundles/server-$(HOST)/setup.sh
	echo 'BASE=$$(dirname $$(readlink -f $$0))' >> bundles/server-$(HOST)/setup.sh
	echo 'TLSOPTS="--tlsverify --tlscacert $(PKI)/ca.pem --tlscert $(PKI)/cert.pem --tlskey $(PKI)/key.pem"' >> bundles/server-$(HOST)/setup.sh
	# GET OPTS FROM DEFAULT
	echo 'OPTS=$$(cat /etc/default/docker | sed -r "s/^[^\"]+\"([^\"]+)\"/\\1/g")' >> bundles/server-$(HOST)/setup.sh
	# REMOVE TLS EXISTING IF EXIST
	echo 'OPTS=$$(echo $$OPTS | sed -r "s/(--tls[^\s-]+)(\s+[^\s-]+)?//g")' >> bundles/server-$(HOST)/setup.sh
	# REMOVE OLD
	echo "sed -ri '/^DOCKER_OPTS/d' /etc/default/docker" >> bundles/server-$(HOST)/setup.sh
	# UPDATE DEFAULT
	echo 'echo DOCKER_OPTS=\"$$OPTS $$TLSOPTS\" >> /etc/default/docker' >>  bundles/server-$(HOST)/setup.sh
	# DEPLOY CERTS
	echo "mkdir -p $(PKI)" >> bundles/server-$(HOST)/setup.sh
	echo 'cp $$BASE/ca.pem $$BASE/cert.pem $$BASE/key.pem $(PKI)/' >> bundles/server-$(HOST)/setup.sh
	# MAKE SCRIPT EXECUTABLE
	chmod +x bundles/server-$(HOST)/setup.sh

dockerclientbundle:
	mkdir -p bundles/client-$(HOST)
	cp certs/client-$(HOST).crt bundles/client-$(HOST)/cert.pem
	cp certs/client-$(HOST).key bundles/client-$(HOST)/key.pem
	cp ca/ca-chain.crt bundles/client-$(HOST)/ca.pem
	echo "#! /bin/bash" > bundles/client-$(HOST)/setup.sh
	echo 'BASE=$$(dirname $$(readlink -f $$0))' >> bundles/client-$(HOST)/setup.sh
	echo 'TLSOPTS="--tlsverify"' >> bundles/client-$(HOST)/setup.sh
	# REMOVE OLD ENV FROM ~/.bashrc
	echo 'sed -ri "/^export DOCKER/d" $$HOME/.bashrc' >> bundles/client-$(HOST)/setup.sh
	# ADD TLS OPTIONS
	echo 'echo export DOCKER_TLS_VERIFY=1 >> $$HOME/.bashrc' >> bundles/client-$(HOST)/setup.sh
	echo 'echo export DOCKER_CERT_PATH=$$HOME/.docker >> $$HOME/.bashrc' >> bundles/client-$(HOST)/setup.sh
	echo 'echo export DOCKER_HOST=tcp://$(HOST):2375 >> $$HOME/.bashrc' >> bundles/client-$(HOST)/setup.sh
	echo 'cp $$BASE/ca.pem $$BASE/cert.pem $$BASE/key.pem $$HOME/.docker/' >> bundles/client-$(HOST)/setup.sh
	# MAKE SCRIPT EXECUTABLE
	chmod +x bundles/client-$(HOST)/setup.sh

clean:
	rm -Rf  etc ca certs crl bundles

.PHONY: ca clientcert deploy2dockerclient removecrlendpoint startcrlendpoint caconfig clientconfig dockerclientbundle revokecert stopcrlendpoint clean crl dockerserverbundle servercert cleandockerclient crlimage dockertls serverconfig 



