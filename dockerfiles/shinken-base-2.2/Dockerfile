# Shinken base image
# VERSION    2.2

FROM                debian:7
MAINTAINER      Shinken
ENV                   TAG 2.2
ENV   SHINKENUID 1003
ENV   SHINKENGID 1003
#########################################################
# Prerequisites
#########################################################
RUN    apt-get update && apt-get -y upgrade && \
           apt-get -y install python-pycurl python-pip git vim-nox python-paramiko sysstat wget curl net-tools\ 
            python-pymongo python-gridfs python-pysqlite2 python-redis sudo

#########################################################
# install shinken
#########################################################

RUN         groupadd -g $SHINKENGID shinken && \
            useradd shinken --gid $SHINKENGID --uid $SHINKENUID && \
            mkdir -p /home/shinken && \
            cd /home/shinken && git clone https://github.com/naparuba/shinken.git && \
            cd /home/shinken/shinken && git checkout tags/$TAG && \
            cd /home/shinken/shinken && python setup.py install && \
            mkdir -p /var/run/shinken /var/log/shinken && \
            chown shinken:shinken /var/run/shinken /var/log/shinken /home/shinken /home/shinken/shinken

##  enable debug on daemons (optional)
RUN   sed -i "s/log_level=.*/log_level=DEBUG/g" /etc/shinken/daemons/pollerd.ini
RUN   sed -i "s/log_level=.*/log_level=DEBUG/g" /etc/shinken/daemons/brokerd.ini
RUN   sed -i "s/log_level=.*/log_level=DEBUG/g" /etc/shinken/daemons/reactionnerd.ini
RUN   sed -i "s/log_level=.*/log_level=DEBUG/g" /etc/shinken/daemons/schedulerd.ini

#########################################################
# plugins
#########################################################

## Nagios plugins
RUN   apt-get -y install nagios-plugins

## manubulon plugins
RUN     wget http://nagios.manubulon.com/check_snmp_load.pl && \
            mv check_snmp_load.pl /usr/lib/nagios/plugins && \
            chmod +x /usr/lib/nagios/plugins/check_snmp_load.pl && \
            wget http://nagios.manubulon.com/check_snmp_storage.pl && \
            mv check_snmp_storage.pl /usr/lib/nagios/plugins && \
            chmod +x /usr/lib/nagios/plugins/check_snmp_storage.pl && \
            mkdir -p /usr/local/nagios && \
            ln -s /usr/lib/nagios/plugins /usr/local/nagios/libexec && \
            wget http://nagios.manubulon.com/check_snmp_mem.pl && \
            mv check_snmp_mem.pl /usr/lib/nagios/plugins && \
            chmod +x /usr/lib/nagios/plugins/check_snmp_mem.pl && \
            wget http://nagios.manubulon.com/check_snmp_mem.pl && \
            mv check_snmp_mem.pl /usr/lib/nagios/plugins && \
            chmod +x /usr/lib/nagios/plugins/check_snmp_mem.pl && \
            wget http://nagios.manubulon.com/check_snmp_process.pl && \
            mv check_snmp_process.pl /usr/lib/nagios/plugins && \
            chmod +x /usr/lib/nagios/plugins/check_snmp_process.pl

## prerequisites for check_mywebsite
RUN     pip install docopt checkmyws-python


#########################################################
## install modules 
#########################################################
RUN     shinken --init && \
            shinken install ip-tag && \
            shinken install ws-arbiter && \
            shinken install pickle-retention-file-generic && \
            shinken install pickle-retention-file-scheduler && \
            shinken install hack-commands-poller-tag-arbiter && \
            shinken install named-pipe && \
            shinken install csv-tag && \
            shinken install hack-poller-tag-by-macros && \
            shinken install file-tag && \
            shinken install mod-mongodb && \
            shinken install webui && \
            shinken install livestatus && \
            shinken install logstore-mongodb && \
            shinken install ui-graphite && \
            shinken install sqlitedb && \
            shinken install graphite && \
            shinken install logstore-sqlite && \
            shinken install sqlitelog && \
            shinken install snapshot-mongodb && \
            shinken install retention-mongodb && \
            shinken install auth-cfg-password && \
            shinken install retention-redis && \
            shinken install ws-arbiter

# enable scheduler retention
RUN      sed -i -E "s/^(\s+modules).*$/\1 pickle-retention-file/g" /etc/shinken/schedulers/scheduler-master.cfg

#########################################################
# packs
#########################################################
RUN     shinken --init && \
            shinken install mongodb && \
            shinken install check_mywebsite && \
            shinken install arbiter2 && \
            shinken install linux-ssh && \
            shinken install linux-snmp && \
            shinken install ldap && \
            shinken install imap && \
            shinken install san-switch && \
            shinken install oracle && \
            shinken install exchange && \
            shinken install windows && \
            shinken install vmware && \
            shinken install ftp && \
            shinken install http && \
            shinken install ssh && \
            shinken install dc && \
            shinken install hpux && \
            shinken install dns && \
            shinken install mysql && \
            shinken install activemq && \
            shinken install memcached && \
            shinken install hp-asm && \
            shinken install pop3 && \
            shinken install dhcp && \
            shinken install smtp && \
            shinken install emc && \
            shinken install mongodb && \
            shinken install ntp && \
            shinken install http-proxy && \
            shinken install tomcat && \
            shinken install cisco && \
            shinken install asterisk && \
            shinken install hp && \
            shinken install postgresql && \
            shinken install hp-blades-chassis && \
            shinken install switch && \
            shinken install mssql && \
            pip install docopt checkmyws-python

#########################################################
# supervisor base 
#########################################################

RUN   pip install supervisor && \
                  echo_supervisord_conf > /etc/supervisord.conf && \
                  echo "[include]" >> /etc/supervisord.conf && \
                  echo "files = supervisord.d/*.conf" >> /etc/supervisord.conf && \
                  mkdir -p /etc/supervisord.d

#########################################################
# sudoers
#########################################################
COPY        sudoers.d.shinken /etc/sudoers.d/shinken
RUN         chmod 440 /etc/sudoers.d/shinken

#########################################################
# Cleanup and Hacks
#########################################################

## remove shinken sources
RUN      rm -Rf /home/shinken/shinken

CMD	["/usr/local/bin/supervisord", "-n", "-c", "/etc/supervisord.conf"]
