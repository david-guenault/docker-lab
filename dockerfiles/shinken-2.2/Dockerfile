# Shinken base image
# VERSION    2.2

FROM                dguenault/centos-ssh:6
MAINTAINER      David GUENAULT
ENV                  TAG 2.2-RC1

# prerequisites
RUN     yum -y install python-pycurl python-setuptools git vim-enhanced python-paramiko sysstat wget curl pymongo pymongo-gridfs net-snmp net-snmp-utils perl-Net-SNMP

# install shinken
RUN     adduser shinken && \
            cd /home/shinken && git clone https://github.com/naparuba/shinken.git && \
            cd /home/shinken/shinken && git checkout tags/$TAG && \
            cd /home/shinken/shinken && python setup.py install

# remove shinken sources
#RUN      rm -Rf /home/shinken/shinken

# create folders
RUN     mkdir -p /var/run/shinken /var/log/shinken && \
            chown shinken:shinken /var/run/shinken /var/log/shinken /home/shinken/shinken

# install supervisor and configuration 
ADD     files/supervisor/supervisord.conf /etc/supervisord.conf 
ADD     files/supervisor/snmpd.conf /etc/supervisord.d/ 

# fix nagios plugins path
RUN    sed -i "s/\/usr\/lib\/nagios\/plugins/\/usr\/lib64\/nagios\/plugins/g" /etc/shinken/resource.d/paths.cfg

# fix snmpd configuration
RUN     sed -i "/^view/d" /etc/snmp/snmpd.conf && \
            echo "view    systemview    included   .1" >> /etc/snmp/snmpd.conf

# generate ssh key pair for shinken user
RUN     su - shinken -c "ssh-keygen -t rsa -f /home/shinken/.ssh/id_rsa -q -N \"\"" && \
            su - shinken -c "cat /home/shinken/.ssh/id_rsa.pub > /home/shinken/.ssh/authorized_keys"

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
#            shinken install livestatus && \
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

# temp : install livestatus from git 1.1
RUN      git clone https://github.com/shinken-monitoring/mod-livestatus.git && \
            cd mod-livestatus && \
            git checkout tags/1.1 && \
            cp -a /mod-livestatus/module /var/lib/shinken/modules/livestatus && \
            chown -R shinken:shinken /var/lib/shinken/modules/livestatus && \
            cp /mod-livestatus/etc/modules/livestatus.cfg /etc/shinken/modules/livestatus.cfg
            
