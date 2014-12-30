# Shinken broker image
# VERSION    2.2

FROM                dguenault/shinken:2.2
MAINTAINER      David GUENAULT
ENV                  TAG 2.2-RC1

# snmp and nagios plugins
RUN     yum -y install python-whisper python-carbon pymongo pymongo-gridfs graphite-web python-sqlite2

# daemons
ADD     files/supervisor/shinken.conf /etc/supervisord.d/
ADD     files/supervisor/carbon-cache.conf /etc/supervisord.d/
ADD     files/supervisor/httpd.conf /etc/supervisord.d/

# fix permission
RUN     chown -R carbon:carbon /var/run/carbon

# port
EXPOSE 7772