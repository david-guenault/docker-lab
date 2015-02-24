ORGANIZATION=BOX4PROD
DOMAIN=box4prod
TLD=com
UNIT=IT
DAYS=3650
SIZE=2048
OPENSSL=/usr/bin/openssl

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
		etc/root-ca.conf
	sed -i \
		-e "s/@DOMAIN@/$(DOMAIN)/g" \
		-e "s/@TLD@/$(TLD)/g" \
		-e "s/@ORGANIZATION@/$(ORGANIZATION)/g" \
		-e "s/@SIZE@/$(SIZE)/g" \
		-e "s/@DAYS@/$(DAYS)/g" \
		etc/signing-ca.conf

serverconfig:
	cp templates/server.conf.template etc/$(HOST).conf
	sed -i \
		-e "s/@DOMAIN@/$(DOMAIN)/g" \
		-e "s/@ORGANIZATION@/$(ORGANIZATION)/g" \
		-e "s/@TLD@/$(TLD)/g" \
		-e "s/@UNIT@/$(UNIT)/g" \
		-e "s/@SIZE@/$(SIZE)/g" \
		-e "s/@CN@/$(HOST)/g" \
		etc/$(HOST).conf

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
    		-out crl/signing-ca.crl	

servercert: serverconfig
	SAN="DNS:$(HOST)" \
	$(OPENSSL) req \
		-new -config etc/$(HOST).conf \
		-out certs/$(HOST).csr \
		-keyout certs/$(HOST).key \
		-nodes \
		-batch && \
	$(OPENSSL) ca \
		-config etc/signing-ca.conf \
		-in certs/$(HOST).csr \
		-out certs/$(HOST).crt \
		-extensions server_ext \
		-batch && \
	cat certs/$(HOST).crt  ca/ca-chain.crt > certs/$(HOST)-chain.crt

pkcs12:
	$(OPENSSL) pkcs12 -export \
    		-name "$(HOST)" \
    		-inkey certs/$(HOST).key \
    		-in certs/$(HOST).crt \
    		-out certs/$(HOST).p12

deploy2consul:
	cp ca/signing-ca.crt ../dockerfiles/consul/ssl/ca.pem
	cp certs/$(HOST)-chain.crt ../dockerfiles/consul/ssl/cert.pem
	cp certs/$(HOST).key ../dockerfiles/consul/ssl/key.pem

dockertls:
	@-echo "**************************************************************************"
	@-echo "Launch docker in tls verify mode for testing purpose"
	@-echo "**************************************************************************"
	@-echo "If you want a more definitive solution :"
	@-echo " > create a folder /etc/pki/docker/"
	@-echo " > Copy the ca, cert and key to this folder"
	@-echo " > Add the following to the DOCKER_OPTS line in /etc/default/docker:"
	@-echo "   --tlsverify --tlscacert /etc/pki/docker/ca-chain.crt --tlscert /etc/pki/docker/[cername].crt --tlskey /etc/pki/docker/[certname].key"
	@-echo "> Restart docker"
	@-echo ""
	@-echo "=> Hit enter to continue <="
	@-read  ""
	@-docker -H tcp://0.0.0.0:2375 --tlsverify --tlscacert ca/ca-chain.crt --tlscert certs/$(HOST).crt --tlskey certs/$(HOST).key -D -d

deploy2dockerclient:
	rm -f ~/.docker/*.pem
	rm -f ~/.docker/*.crt
	rm -f ~/.docker/*.key
	cp ca/ca-chain.crt ~/.docker/ca.pem
	certs/$(HOST).crt  ~/.docker/cert.pem
	certs/$(HOST).key ~/.docker/key.pem
	echo "DOCKER_HOST=tcp://$(HOST):$(PORT)" >> ~/.bashrc
	echo "DOCKER_TLS_VERIFY=1" >> ~/.bashrc


clean:
	rm -Rf  etc ca certs crl bundles

.PHONY: ca clean cert caconfig serverconfig crl bundle



