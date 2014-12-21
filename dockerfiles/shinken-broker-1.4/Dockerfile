# Shinken broker image
# VERSION    1.4

FROM                dguenault/shinken:1.4.4
MAINTAINER      David GUENAULT

# snmp and nagios plugins
RUN     yum -y install python-whisper python-carbon pymongo pymongo-gridfs

# daemons
ADD     files/supervisor/shinken.conf /etc/supervisord.d/

# port
EXPOSE 7772


