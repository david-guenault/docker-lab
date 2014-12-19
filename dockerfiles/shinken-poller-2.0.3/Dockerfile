# Shinken with just poller shinken 2.0.3 base image
# modules
#	
# VERSION	2.0.3

FROM     	dguenault/shinken:2.0.3	
MAINTAINER	David GUENAULT

# prerequisites
RUN     yum -y install nagios-plugins-all

# install supervisor configuration 
ADD     files/supervisor/shinken-poller.conf /etc/supervisord.d/

# fix some path and permisions
RUN     chown root:shinken /usr/lib64/nagios/plugins/check_icmp
RUN     chmod u+s /usr/lib64/nagios/plugins/check_icmp

# install shinken modules
RUN	su - shinken -c "shinken --init && \
	shinken install linux-ssh && \
	shinken install linux-snmp" 
