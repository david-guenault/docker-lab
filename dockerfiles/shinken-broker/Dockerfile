# Shinken with just poller shinken 2.0.3 base image
# modules
#	
# VERSION	2.0.3

FROM     	dguenault/shinken:2.0.3	
MAINTAINER	David GUENAULT

# install supervisor configuration 
ADD     files/supervisor/shinken-broker.conf /etc/supervisord.d/

# install shinken modules
RUN	su - shinken -c "shinken --init && \
	shinken install webui && \
	shinken install auth-cfg-password && \
	shinken install logstore-sqlite" 
