ORGANIZATION=BOX4PROD
DOMAIN=box4prod
TLD=com
UNIT=IT
DAYS=3650
SIZE=2048
OPENSSL=/usr/bin/openssl
DOCKER=/usr/bin/docker
PKI=/etc/pki/docker

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
	cp templates/server.conf.template etc/server-$(HOST).conf
	sed -i \
		-e "s/@DOMAIN@/$(DOMAIN)/g" \
		-e "s/@ORGANIZATION@/$(ORGANIZATION)/g" \
		-e "s/@TLD@/$(TLD)/g" \
		-e "s/@UNIT@/$(UNIT)/g" \
		-e "s/@SIZE@/$(SIZE)/g" \
		-e "s/@CN@/$(HOST)/g" \
		-e "s/@HOST@/$(HOST)/g" \
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
    		-out crl/signing-ca.crl	

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

dockerbundle:
	rm -Rf bundles/$(HOST)
	mkdir -p bundles/$(HOST)
	cp certs/server-$(HOST).csr bundles/$(HOST)/cert.pem
	cp certs/server-$(HOST).key bundles/$(HOST)/key.pem
	cp ca/ca-chain.crt bundles/$(HOST)/ca.pem
	echo "#! /bin/bash" > bundles/$(HOST)/setup.sh
	echo 'BASE=$$(dirname $$(readlink -f $$0))' >> bundles/$(HOST)/setup.sh
	echo 'TLSOPTS="--tlsverify --tlscacert $(PKI)/ca.pem --tlscert $(PKI)/cert.pem --tlskey $(PKI)/key.pem"' >> bundles/$(HOST)/setup.sh
	echo "sed -ri 's/(--tls[^\s-]+)(\s+[^\s-]+)?//g' /etc/default/docker" >> bundles/$(HOST)/setup.sh
	echo 'OPTS=$$(cat /etc/default/docker | sed -r "s/.*\"([^\"]+)\"/\\1/g")' >> bundles/$(HOST)/setup.sh
	echo 'sed -ri "/^DOCKER_OPTS/d" /etc/default/docker' >> bundles/$(HOST)/setup.sh
	echo 'echo DOCKER_OPTS=\"$$OPTS $$TLSOPTS\" >> /etc/default/docker' >>  bundles/$(HOST)/setup.sh
	echo "mkdir -p $(PKI)" >> bundles/$(HOST)/setup.sh
	echo 'cp $$BASE/ca.pem $$BASE/cert.pem $$BASE/key.pem $(PKI)/' >> bundles/$(HOST)/setup.sh
	chmod +x bundles/$(HOST)/setup.sh

clean:
	rm -Rf  etc ca certs crl

.PHONY: ca clean clientcert crl dockerbundle servercert caconfig cleandockerclient clientconfig deploy2dockerclient dockertls serverconfig 




