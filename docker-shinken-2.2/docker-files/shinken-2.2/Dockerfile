# Shinken base image
# VERSION    2.2

FROM                debian:7
MAINTAINER      David GUENAULT
ENV                   TAG 2.2

# update base image
RUN    apt-get update && apt-get -y upgrade

# prerequisites
RUN     apt-get -y install python-pycurl python-pip git vim-nox python-paramiko sysstat wget curl \ 
            python-pymongo python-gridfs python-pysqlite2

# install shinken
RUN     useradd shinken && \
            mkdir -p /home/shinken && \
            cd /home/shinken && git clone https://github.com/naparuba/shinken.git && \
            cd /home/shinken/shinken && git checkout tags/$TAG && \
            cd /home/shinken/shinken && python setup.py install

RUN     mkdir -p /var/run/shinken /var/log/shinken && \
            chown shinken:shinken /var/run/shinken /var/log/shinken /home/shinken /home/shinken/shinken

# enable debug on daemons 
RUN   sed -i "s/log_level=.*/log_level=DEBUG/g" /etc/shinken/daemons/pollerd.ini
RUN   sed -i "s/log_level=.*/log_level=DEBUG/g" /etc/shinken/daemons/brokerd.ini
RUN   sed -i "s/log_level=.*/log_level=DEBUG/g" /etc/shinken/daemons/reactionnerd.ini
RUN   sed -i "s/log_level=.*/log_level=DEBUG/g" /etc/shinken/daemons/schedulerd.ini

# fix nagios plugins path
RUN    sed -i "s/\/usr\/lib\/nagios\/plugins/\/usr\/lib64\/nagios\/plugins/g" /etc/shinken/resource.d/paths.cfg

# install modules 
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

# packs
RUN     shinken --init && \
            shinken install mongodb && \
            shinken install check_mywebsite && \
            shinken install arbiter2 && \
            shinken install linux-ssh && \
            shinken install linux-snmp && \
            pip install docopt checkmyws-python

# remove shinken sources
RUN      rm -Rf /home/shinken/shinken

# # temp : install livestatus from git 1.1
# RUN      git clone https://github.com/shinken-monitoring/mod-livestatus.git && \
#             cd mod-livestatus && \
#             # git checkout tags/1.1 && \
#             cp -a /mod-livestatus/module /var/lib/shinken/modules/livestatus && \
#             chown -R shinken:shinken /var/lib/shinken/modules/livestatus && \
#             cp /mod-livestatus/etc/modules/livestatus.cfg /etc/shinken/modules/livestatus.cfg
            
