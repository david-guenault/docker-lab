# Shinken from master branch 
# VERSION	2.0.3

FROM     	centos:centos6
MAINTAINER	David GUENAULT
# epel 
RUN     yum -y install http://mirrors.ircam.fr/pub/fedora/epel/6/i386/epel-release-6-8.noarch.rpm && \
	yum clean all

# prerequisites
RUN     yum -y install openssh-server python-pip

# sshd agent
RUN 	mkdir /var/run/sshd
RUN 	echo 'root:root' | chpasswd

# generate host key files
RUN	ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key -q -N ""
RUN	ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -q -N ""

# fix 
RUN 	sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
RUN 	sed -ri 's/#UsePAM no/UsePAM no/g' /etc/ssh/sshd_config

# install supervisor and configuration 
RUN     pip install supervisor
RUN     mkdir -p /etc/supervisord.d
RUN     mkdir -p /var/log/supervisord
ADD     files/supervisor/supervisord.conf /etc/supervisord.conf
ADD     files/supervisor/sshd.conf /etc/supervisord.d/

# Expose needed tcp ports
EXPOSE 22

CMD ["supervisord", "-c", "/etc/supervisord.conf", "-n"]
