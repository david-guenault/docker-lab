# Shinken from master branch 
# VERSION	1.4.4

FROM     	dguenault/centos-ssh:6
MAINTAINER	David GUENAULT

# prerequisites
RUN     yum -y install python-pycurl python-setuptools git vim-enhanced python-paramiko sysstat wget curl python-pyro net-snmp net-snmp-utils perl-Net-SNMP

# install shinken
RUN	adduser shinken
RUN	cd /home/shinken && git clone https://github.com/naparuba/shinken.git
RUN	cd /home/shinken/shinken && git checkout tags/1.4.4
RUN     cd /home/shinken/shinken && python setup.py install

# create folders
RUN     mkdir -p /var/run/shinken /var/log/shinken
RUN     chown shinken:shinken /var/run/shinken /var/log/shinken /home/shinken/shinken

# install supervisor and configuration 
ADD     files/supervisor/supervisord.conf /etc/supervisord.conf
ADD     files/supervisor/snmpd.conf /etc/supervisord.d/

# fix plugins path in shinken resources config 
RUN	sed -i "s/\/usr\/lib\/nagios\/plugins/\/usr\/lib64\/nagios\/plugins/g" /etc/shinken/resource.cfg

# little fix on linux pack
RUN     sed -i "s/-q -k -y/-q -k -y -g -2/g" /etc/shinken/packs/os/linux/commands.cfg

# fix snmpd configuration
RUN     sed -i "/^view/d" /etc/snmp/snmpd.conf
RUN     echo "view    systemview    included   .1" >> /etc/snmp/snmpd.conf

