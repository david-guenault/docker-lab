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

# create folders
RUN     mkdir -p /var/run/shinken /var/log/shinken && \
            chown shinken:shinken /var/run/shinken /var/log/shinken /home/shinken/shinken

# install supervisor and configuration 
ADD     files/supervisor/supervisord.conf /etc/supervisord.conf 
ADD     files/supervisor/sshd.conf /etc/supervisord.d/ 
ADD     files/supervisor/snmpd.conf /etc/supervisord.d/ 

# fix snmpd configuration
RUN     sed -i "/^view/d" /etc/snmp/snmpd.conf && \
            echo "view    systemview    included   .1" >> /etc/snmp/snmpd.conf

# fix nagios plugins path
RUN    sed -i "s/\/usr\/lib\/nagios\/plugins/\/usr\/lib64\/nagios\/plugins/g" /etc/shinken/resource.d/paths.cfg

# generate ssh key pair
RUN     su - shinken -c "ssh-keygen -t rsa -f /home/shinken/.ssh/id_rsa -q -N \"\"" && \
            su - shinken -c "cat /home/shinken/.ssh/id_rsa.pub > /home/shinken/.ssh/authorized_keys"
