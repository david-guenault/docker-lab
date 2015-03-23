include ../common/Makefile
NAME = ces
RUNNAME = ces
TAG = 3.0.0
DOCKER=/usr/bin/docker
SSHPASSWORD=centreon
SUPERVISORUSER=admin
SUPERVISORPASSWORD=admin
NAGVISUSER=nagvis
NAGVISPASSWORD=nagvis

configure:
	cp Dockerfile.template Dockerfile
	sed -i "s/@SSHPASSWORD@/$(SSHPASSWORD)/g" Dockerfile
	sed -i "s/@NAGVISUSER@/$(NAGVISUSER)/g" Dockerfile
	sed -i "s/@NAGVISPASSWORD@/$(NAGVISPASSWORD)/g" Dockerfile
	cp nagvis.ini.php.template nagvis.ini.php
	sed -i "s/@NAGVISUSER@/$(NAGVISUSER)/g" nagvis.ini.php
	sed -i "s/@NAGVISPASSWORD@/$(NAGVISPASSWORD)/g" nagvis.ini.php
	cp supervisord.conf.template supervisord.conf
	sed -i "s/@SUPERVISORUSER@/$(SUPERVISORUSER)/g" supervisord.conf
	sed -i "s/@SUPERVISORPASSWORD@/$(SUPERVISORPASSWORD)/g" supervisord.conf

rebuild: 
	@-$(MAKE) kill
	@-$(MAKE) rm 
	@-$(MAKE) configure 
	@-$(MAKE) build