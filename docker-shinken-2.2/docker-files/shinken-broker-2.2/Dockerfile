# Shinken broker image
# VERSION    2.2

FROM                dguenault/shinken:2.2
MAINTAINER      David GUENAULT
ENV                  TAG 2.2-RC1

# snmp and nagios plugins
RUN     yum -y install python-whisper python-carbon pymongo pymongo-gridfs graphite-web python-sqlite2

# init graphite db
RUN     sed -i "s#\(carbon.*\)\(/sbin/nologin\)#\1/bin/bash#g" /etc/passwd && \
             sed -i "s#\(apache.*\)\(/sbin/nologin\)#\1/bin/bash#g" /etc/passwd && \
             su - apache -c "cd /usr/lib/python2.6/site-packages/graphite &&  python manage.py syncdb --noinput" 

# daemons
ADD     files/supervisor/shinken.conf /etc/supervisord.d/
ADD     files/supervisor/carbon-cache.conf /etc/supervisord.d/
ADD     files/supervisor/httpd.conf /etc/supervisord.d/

# fix permission
RUN     chown -R carbon:carbon /var/run/carbon

# port
EXPOSE 7772