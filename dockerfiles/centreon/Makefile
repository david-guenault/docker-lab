include ../common/Makefile
NAME = ces
RUNNAME = ces
TAG = 3.0.0
DOCKER=/usr/bin/docker
SSHPASSWORD=centreon
SUPERVISORUSER=admin
SUPERVISORPASSWORD=admin

configure:
	cp Dockerfile.template Dockerfile
	sed -i "s/@SSHPASSWORD@/$(SSHPASSWORD)/g" Dockerfile
	cp supervisord.conf.template supervisord.conf
	sed -i "s/@SUPERVISORUSER@/$(SUPERVISORUSER)/g" supervisord.conf
	sed -i "s/@SUPERVISORPASSWORD@/$(SUPERVISORPASSWORD)/g" supervisord.conf

