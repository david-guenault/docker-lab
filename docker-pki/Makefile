ORGANIZATION=BOX4PROD
DOMAIN=box4prod.com
DAYS=3650
SIZE=2048
OPENSSL=/usr/bin/openssl

caconfig:
	mkdir -p etc
	cp templates/root-ca.conf.template etc/root-ca.conf
	cp templates/signing-ca.conf.template etc/signing-ca.conf
	sed -i \
		-e "s/@DOMAIN@/$(DOMAIN)/g" \
		-e "s/@ORGANIZATION@/$(ORGANIZATION)/g" \
		-e "s/@SIZE@/$(SIZE)/g" \
		-e "s/@DAYS@/$(DAYS)/g" \
		etc/root-ca.conf
	sed -i \
		-e "s/@DOMAIN@/$(DOMAIN)/g" \
		-e "s/@ORGANIZATION@/$(ORGANIZATION)/g" \
		-e "s/@SIZE@/$(SIZE)/g" \
		-e "s/@DAYS@/$(DAYS)/g" \
		etc/signing-ca.conf

serverconfig:
	cp templates/server.conf.template etc/$(HOST).conf
	sed -i \
		-e "s/@DOMAIN@/$(DOMAIN)/g" \
		-e "s/@ORGANIZATION@/$(ORGANIZATION)/g" \
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
    		-batch
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
		-batch

bundle:
	mkdir -p bundles/$(HOST)
	cp certs/$(HOST).crt certs/$(HOST).key bundles/$(HOST)/
	cp ca/signing-ca/01.pem bundles/$(HOST)/ca.pem

clean:
	rm -Rf  etc ca certs crl

.PHONY: ca clean cert caconfig serverconfig crl bundle



