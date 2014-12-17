# Shinken from master branch 
# VERSION	1.4.4

FROM     	dguenault/centos-ssh:6
MAINTAINER	David GUENAULT

# prerequisites
RUN     yum -y install python-pycurl python-setuptools git vim-enhanced python-paramiko sysstat wget curl python-pyro

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
ADD     files/supervisor/sshd.conf /etc/supervisord.d/

# config 
RUN	sed -i "s/\/usr\/lib\/nagios\/plugins/\/usr\/lib64\/nagios\/plugins/g" /etc/shinken/resource.cfg

# modules and packs
# RUN	su - shinken -c "shinken --init && \
# 	shinken install linux-ssh && \
# 	shinken install webui && \
# 	shinken install auth-cfg-password && \
# 	shinken install logstore-sqlite && \
# 	shinken install livestatus"


# Expose needed tcp ports
EXPOSE  7766
EXPOSE  7767
EXPOSE  7768
EXPOSE  7769
EXPOSE  7770
EXPOSE  7771
EXPOSE  7772

