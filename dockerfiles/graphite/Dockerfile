FROM    debian:latest
RUN DEBIAN_FRONTEND=noninteractive apt-get -y update

ENV TIMEZONE UTC

# Install required packages
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install \
            python2.6 \
            python-pip \
            python-cairo \
            python-django \ 
            python-django-tagging \
            python-twisted \ 
            python-memcache \
            python-pysqlite2 \ 
            python-simplejson \
            apache2 \
            apache2 libapache2-mod-wsgi && \
       pip install supervisor && \
       pip install https://github.com/graphite-project/ceres/tarball/master && \
       pip install whisper && \
       pip install carbon && \
       pip install graphite-web

# apache conf
RUN a2dissite 000-default &&\
        cp /opt/graphite/examples/example-graphite-vhost.conf /etc/apache2/sites-available/graphite && \
        a2ensite graphite


# Add system service config
RUN mkdir -p /var/log/supervisor
COPY supervisord/supervisord.conf /etc/
COPY supervisord/apache.conf /etc/supervisord.d/
COPY supervisord/carbon-cache.conf /etc/supervisord.d/
# COPY supervisord/graphite-web.conf /etc/supervisord.d/

# graphite settings
RUN cd /opt/graphite/conf && \
        cp storage-schemas.conf.example storage-schemas.conf && \
        cp storage-aggregation.conf.example storage-aggregation.conf && \
        cp carbon.conf.example carbon.conf && \
        cp graphite.wsgi.example graphite.wsgi && \
        cd /opt/graphite/webapp/graphite && \
        cp local_settings.py.example local_settings.py && \
        # sed -i -E "s/^TIME_ZONE.*$/TIME_ZONE = '"$(cat /etc/timezone)"'" local_settings.py  && \
        KEY=$(python -c 'import random; print "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])') && \
        sed -i -E "s/SECRET_KEY = 'UNSAFE_DEFAULT'/SECRET_KEY = '"$KEY"'" local_settings.py

# init
RUN cd /opt/graphite/webapp/graphite && \
        python manage.py syncdb --noinput && \
        chmod +x /opt/graphite/conf/graphite.wsgi && \
        chown -R www-data:www-data /opt/graphite/webapp/ /opt/graphite/storage/

# fix apache2 conf
RUN  sed -i -E "s/WSGISocketPrefix.*$/WSGISocketPrefix \/var\/run/g" /etc/apache2/sites-available/graphite

# Nginx
EXPOSE  :80
# Carbon line receiver port
EXPOSE  :2003
# Carbon pickle receiver port
EXPOSE  :2004
# Carbon cache query port
EXPOSE  :7002

CMD ["/usr/local/bin/supervisord", "-n", "-c", "/etc/supervisord.conf"]