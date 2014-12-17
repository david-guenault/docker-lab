BROWSER=/usr/bin/google-chrome-beta

webui:
	$(BROWSER) http://$$(dig @172.17.42.1 shinken.dock2dns.lan | grep "^shinken" | awk '{print $$5}'):7767
thruk:
	$(BROWSER) http://$$(dig @172.17.42.1 thruk.dock2dns.lan | grep "^thruk" | awk '{print $$5}')/thruk/
supervisor:
	$(BROWSER) http://admin:supervisor@$$(dig @172.17.42.1 shinken.dock2dns.lan | grep "^shinken" | awk '{print $$5}'):9001

.PHONY: webui thruk supervisor
