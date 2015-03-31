FROM                centos:6.6 
MAINTAINER     David GUENAULT

# manage yum repositories
RUN   rpm -Uvh http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el6.rf.x86_64.rpm && \
      rpm -Uvh http://fr2.rpmfind.net/linux/epel/6/i386/epel-release-6-8.noarch.rpm && \
      yum-config-manager --disable rpmforge && \
      yum-config-manager --disable epel && \
      yum -y update

# supervisord configuration files
COPY  shinken-enterprise-2.03-6.el6.x86_64.rpm /root/shinken-enterprise-2.03-6.el6.x86_64.rpm

# install pip and supervisor
RUN   yum -y --enablerepo="epel" install python-pip && \
      pip install supervisor && \
      mkdir -p /etc/supervisord.d

# cleanup
RUN   rm -Rf /tmp/*

# command 
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisord.d/supervisord.conf"]
