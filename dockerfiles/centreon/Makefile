include ../common/Makefile
NAME = ces
RUNNAME = ces
TAG = 3.0.0
DOCKER=/usr/bin/docker
SSHPASSWORD=centreon
SUPERVISORUSER=admin
SUPERVISORPASSWORD=admin
NAGVISUSER=cnagvis
NAGVISPASSWORD=cnagvis
NAGVISDBUSER=nagvis
NAGVISDBPASSWORD=nagvis
NAGVISADMINUSER=admin
NAGVISADMINPASSWORD=admin
NAGVISPASSWORDSALT=29d58ead6a65f5c00342ae03cdc6d26565e20954

configure:
	cp Dockerfile.template Dockerfile && \
	sed -i "s/@SALT@/$(NAGVISPASSWORDSALT)/g" Dockerfile && \
	sed -i "s/@SSHPASSWORD@/$(SSHPASSWORD)/g" Dockerfile && \
	sed -i "s/@NAGVISUSER@/$(NAGVISUSER)/g" Dockerfile && \
	sed -i "s/@NAGVISPASSWORD@/$(NAGVISPASSWORD)/g" Dockerfile && \
	sed -i "s/@NAGVISDBUSER@/$(NAGVISDBUSER)/g" Dockerfile && \
	sed -i "s/@NAGVISDBPASSWORD@/$(NAGVISDBPASSWORD)/g" Dockerfile && \
	cp nagvis.ini.php.template nagvis.ini.php && \
	sed -i "s/@NAGVISDBUSER@/$(NAGVISDBUSER)/g" nagvis.ini.php && \
	sed -i "s/@NAGVISDBPASSWORD@/$(NAGVISDBPASSWORD)/g" nagvis.ini.php && \
	cp supervisord.conf.template supervisord.conf && \
	sed -i "s/@SUPERVISORUSER@/$(SUPERVISORUSER)/g" supervisord.conf && \
	sed -i "s/@SUPERVISORPASSWORD@/$(SUPERVISORPASSWORD)/g" supervisord.conf && \
	cp nagvis.schema.sql.template nagvis.schema.sql && \
	HASH=$$(echo -n "$(NAGVISPASSWORDSALT)$(NAGVISADMINPASSWORD)" |  openssl dgst -sha1 | awk '{print $$2}') && \
	sed -i "s/@NAGVISADMINUSER@/$(NAGVISADMINUSER)/g" nagvis.schema.sql && \
	sed -i "s/@NAGVISADMINHASH@/$$HASH/g" nagvis.schema.sql && \
	HASH=$$(echo -n "$(NAGVISPASSWORDSALT)$(NAGVISPASSWORD)" |  openssl dgst -sha1 | awk '{print $$2}') && \
	sed -i "s/@NAGVISUSER@/$(NAGVISUSER)/g" nagvis.schema.sql && \
	sed -i "s/@NAGVISHASH@/$$HASH/g" nagvis.schema.sql 

rebuild: 
	@-$(MAKE) kill
	@-$(MAKE) rm 
	@-$(MAKE) configure 
	@-$(MAKE) build

firstrun:
	$(MAKE) initces
	sleep 2
	$(MAKE) runces

initces:
	$(DOCKER) create \
	-v /tmp -v /var/lib/mysql \
	-v /var/lib/centreon \
	-v /var/lib/centreon-broker \
	-v /var/lib/centreon-engine \
	-v /var/log \
	-v /usr/local/nagvis/etc \
	-v /usr/local/nagvis/var \
	-v /etc/centreon \
	-v /usr/share/centreon \
	-v /usr/share/centreon-engine \
	-v /usr/local/nagvis/share/userfiles \
	--name $(RUNNAME)data \
	--entrypoint "/bin/bash" \
	$(IMAGE)

rmdata:
	$(DOCKER) rm $(RUNNAME)data

runces:
	$(DOCKER) run -d --name $(RUNNAME) --hostname $(RUNNAME) --volumes-from $(RUNNAME)data -p 80:80 $(IMAGE)

startces:
	$(DOCKER) start $(RUNNAME)

stopces:
	$(DOCKER) stop $(RUNNAME)

restartces:
	@-$(MAKE) stopces
	sleep 5
	@-$(MAKE) startces