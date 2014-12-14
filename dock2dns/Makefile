BRIDGE=172.17.42.1
DNS=10.20.0.1:53
DOMAIN=dock2dns.lan

config:
	cat fig.yml.in | sed -e "s/@BRIDGE@/$(BRIDGE)/g" -e "s/@DNS@/$(DNS)/g" -e "s/@DOMAIN@/$(DOMAIN)/g" > fig.yml
	cat resolv.conf.in | sed -e "s/@BRIDGE@/$(BRIDGE)/g" -e "s/@DOMAIN@/$(DOMAIN)/g" > resolv.conf

clean:
	rm -f resolv.conf fig.yml

image:
	cp dock2dns/dock2dns.py ../dockerfiles/dock2dns/files/dock2dns.py
	cd ../dockerfiles/dock2dns && \
	$(MAKE) clean && \
	$(MAKE) build

.PHONY: config clean
