# Shinken Arbiter
# VERSION	1.4.4

FROM     	                 dguenault/shinken:1.4.4
MAINTAINER	David GUENAULT

# snmp and nagios plugins
RUN     yum -y install pymongo pymongo-gridfs

# supervisord config for arbiter daemon
ADD     files/supervisor/shinken.conf /etc/supervisord.d/

# Expose needed tcp ports
EXPOSE  7770
