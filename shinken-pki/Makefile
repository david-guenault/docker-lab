ORGANIZATION=SHINKEN
DOMAIN=shinken-monitoring
TLD=org
UNIT=IT
DAYS=3650
SIZE=2048
OPENSSL=/usr/bin/openssl
HOST=shinken

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

ca:
	$(MAKE) caconfig HOST=$(HOST)
	mkdir -p ca/root-ca/private ca/root-ca/db certs && \
	chmod 700 ca/root-ca/private && \
	cp /dev/null ca/root-ca/db/root-ca.db && \
	cp /dev/null ca/root-ca/db/root-ca.db.attr && \
	echo 01 > ca/root-ca/db/root-ca.crt.srl && \
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
	mkdir -p ca/signing-ca/private ca/signing-ca/db certs && \
	chmod 700 ca/signing-ca/private && \
	cp /dev/null ca/signing-ca/db/signing-ca.db && \
	cp /dev/null ca/signing-ca/db/signing-ca.db.attr && \
	echo 01 > ca/signing-ca/db/signing-ca.crt.srl && \
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

servercert: 
	$(MAKE) serverconfig HOST=$(HOST)
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

bundle:
	mkdir -p bundles/$(HOST) && \
	cp certs/server-$(HOST).crt bundles/$(HOST)/server.crt && \
	cp certs/server-$(HOST).key bundles/$(HOST)/server.key && \
	cp ca/ca-chain.crt bundles/$(HOST)/ca.pem


clean:
	rm -Rf  etc ca certs bundles

.PHONY: ca caconfig clean servercert serverconfig bundle



