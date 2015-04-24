FROM		dguenault/centos-ssh:6	
MAINTAINER 	David GUENAULT <david.guenault@gmail.com>

ENV THRUKVER 1.88-3 

RUN    	yum -y install http://download.thruk.org/pkg/v$THRUKVER/rhel6/x86_64/thruk-$THRUKVER.rhel6.x86_64.rpm && \
	yum -y install httpd python-pip 

EXPOSE 80

ADD	files/supervisor/httpd.conf /etc/supervisord.d/

