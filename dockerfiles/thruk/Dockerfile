FROM		dguenault/centos-ssh:6	
MAINTAINER 	David GUENAULT <david.guenault@gmail.com>

RUN    	yum -y install http://www.thruk.org/files/pkg/v1.84-6/rhel6/x86_64/thruk-1.84-6.rhel6.x86_64.rpm && \
	yum -y install httpd python-pip 

ADD	files/supervisor/httpd.conf /etc/supervisord.d/

