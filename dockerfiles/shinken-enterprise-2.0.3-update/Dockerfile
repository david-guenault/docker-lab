FROM centos:6.6
MAINTAINER David GUENAULT

COPY    shinken-enterprise-2.03-update.tar.gz /tmp/
COPY    user.key /tmp/
COPY    mongo.repo.conf /etc/yum.repos.d/mongo.repo

# prerequisites
RUN      yum -y install https://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm && \
            yum -y install tar gunzip which mongodb-org python-gevent python-pip wget && \
            pip install supervisor 

# vmware sdk
# RUN      cd /tmp && \
#              wget http://www.shinken-monitoring.org/archives/VMware-vSphere-SDK-for-Perl-5.1.0-780721.x86_64.tar.gz && \
#              tar zxvf VMware-vSphere-SDK-for-Perl-5.1.0-780721.x86_64.tar.gz

# shinken enterprise
RUN     cd /tmp && \
            tar zxvf shinken-enterprise-2.03-update.tar.gz && \
            cd update && \
            yum -y localinstall shinken-enterprise-2.03-11.el6.x86_64.rpm && \
            cp /tmp/user.key /etc/shinken/user.key && \
            rm -Rf /tmp/shinken-enterprise-2.03-update* &&\
            rm -f /tmp/user.key

# graphite
RUN     yum -y install gcc python-devel && \
           pip install https://github.com/graphite-project/ceres/tarball/master && \
           pip install whisper && \
           pip install carbon && \
           pip install graphite-web && \
           pip install pytz 

# graphite web
# RUN a2dissite 000-default &&\
#         cp /opt/graphite/examples/example-graphite-vhost.conf /etc/apache2/sites-available/graphite && \
#         a2ensite graphite

# # graphite settings
# RUN cd /opt/graphite/conf && \
#         cp storage-schemas.conf.example storage-schemas.conf && \
#         cp storage-aggregation.conf.example storage-aggregation.conf && \
#         cp carbon.conf.example carbon.conf && \
#         cp graphite.wsgi.example graphite.wsgi && \
#         cd /opt/graphite/webapp/graphite && \
#         cp local_settings.py.example local_settings.py && \
#         # sed -i -E "s/^TIME_ZONE.*$/TIME_ZONE = '"$(cat /etc/timezone)"'" local_settings.py  && \
#         KEY=$(python -c 'import random; print "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])') && \
#         sed -i -E "s/SECRET_KEY = 'UNSAFE_DEFAULT'/SECRET_KEY = '"$KEY"'/g" local_settings.py

# # fix apache2 conf graphite web
# RUN  sed -i -E "s/WSGISocketPrefix.*$/WSGISocketPrefix \/var\/run/g" /etc/apache2/sites-available/graphite

# init graphite
# RUN cd /opt/graphite/webapp/graphite && \
#         python manage.py syncdb --noinput && \
#         chmod +x /opt/graphite/conf/graphite.wsgi && \
#         chown -R www-data:www-data /opt/graphite/webapp/ /opt/graphite/storage/

# supervisor
RUN     mkdir -p /etc/supervisord.d 
COPY    supervisor/supervisord.conf /etc/
COPY    supervisor/shinken.conf /etc/supervisord.d/
COPY    supervisor/mongodb.conf /etc/supervisord.d/
# COPY    supervisor/graphite.conf /etc/supervisord.d/

# sudoers
COPY    sudoers.d.shinken /etc/sudoers.d/shinken

# fix some little things
RUN     sed -i -E "s/Livestatus,?//g" /etc/shinken/brokers/broker-master.cfg && \
            sed -i -E "s/fork=.*$/fork=false/g" /etc/mongod.conf && \
            # sed -i -E "s/PLUGINSDIR/NAGIOSPLUGINS/g" /etc/shinken/packs/linux-ssh/commands.cfg && \
            # sed -i -E "s/PLUGINSDIR/NAGIOSPLUGINS/g" /etc/shinken/packs/http/commands.cfg && \
            # sed -i -E "s/PLUGINSDIR/NAGIOSPLUGINS/g" /etc/shinken/packs/hp-printers/commands.cfg && \
            echo "shinken ALL= NOPASSWD: /usr/bin/supervisorctl *" >> /etc/sudoers.d/shinken && \
            sed -i -E "s/sudo \/etc\/init.d\/shinken reload/sudo supervisorctl restart shinken:shinken-arbiter/g" /etc/shinken/commands.cfg && \
            sed -i -E "s/sudo \/etc\/init.d\/shinken restart/sudo supervisorctl restart shinken:shinken-arbiter/g" /etc/shinken/commands.cfg && \
            mkdir -p /var/lib/shinken/doc && \
            chown shinken:shinken /var/lib/shinken/doc

# packs
RUN     mkdir -p /var/lib/shinken/inventory && \
            mkdir -p /var/lib/shinken/doc && \
            chown -R shinken:shinken /var/lib/shinken && \
            shinken --init && \
            shinken install check_mywebsite && \
            pip install docopt && \
            pip install checkmyws-python && \
            chown -R shinken:shinken /etc/shinken

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisord.conf"]

