# Shinken base image
# VERSION    2.2

FROM                debian:7
MAINTAINER      Shinken
ENV                   TAG 2.2

#########################################################
# Prerequisites
#########################################################
RUN    apt-get update && apt-get -y upgrade && \
           apt-get -y install python-pycurl python-pip git vim-nox python-paramiko sysstat wget curl \ 
            python-pymongo python-gridfs python-pysqlite2

#########################################################
# install shinken
#########################################################

RUN     useradd shinken && \
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
            shinken install pickle-retention-file-generic && \
            shinken install graphite && \
            shinken install logstore-sqlite && \
            shinken install sqlitelog && \
            shinken install snapshot-mongodb && \
            shinken install retention-mongodb && \
            shinken install auth-cfg-password

#########################################################
# packs
#########################################################
RUN     shinken --init && \
            shinken install mongodb && \
            shinken install check_mywebsite && \
            shinken install arbiter2 && \
            shinken install linux-ssh && \
            shinken install linux-snmp && \
            pip install docopt checkmyws-python

#########################################################
# Cleanup and Hacks
#########################################################

## remove shinken sources
RUN      rm -Rf /home/shinken/shinken