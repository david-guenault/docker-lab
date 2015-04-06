FROM    dguenault/shinken-base:2.2
MAINTAINER David GUENAULT

ENV     DEBIAN_FRONTEND noninteractive
ENV     SSHPASSWORD root
ENV     NAGVISVERSION 1.8.2
ENV     NAGVISSALT 29d58ead6a65f5c00342ae03cdc6d26565e20954

# upgrade
RUN      apt-get update && apt-get -y upgrade

# some prerequisites
RUN     apt-get install -y snmpd python-pip openssh-server sudo

# Install thruk
RUN     gpg --keyserver keys.gnupg.net --recv-keys F8C1CA08A57B9ED7 && \
            gpg --armor --export F8C1CA08A57B9ED7 | apt-key add - && \
            echo 'deb http://labs.consol.de/repo/stable/debian wheezy main' >> /etc/apt/sources.list && \
            apt-get update && \
            apt-get -y --force-yes install thruk 

#openssh-server
RUN     mkdir /var/run/sshd && \
            echo "root:$SSHPASSWORD" | chpasswd && \
            echo 'PermitRootLogin yes' /etc/ssh/sshd_config && \
            /etc/init.d/ssh start && /etc/init.d/ssh stop && \
            su -c "ssh-keygen -t rsa -N '' -f /home/shinken/.ssh/id_rsa" - shinken && \ 
            sed -i "s/usePAM yes/usePam no/g" /etc/ssh/sshd_config && \
            cat /home/shinken/.ssh/id_rsa.pub > /home/shinken/.ssh/authorized_keys && \
            chown -R shinken:shinken /home/shinken/.ssh && \
            chmod 0600 /home/shinken/.ssh/authorized_keys /home/shinken/.ssh/id_rsa

# enable shinken modules
RUN     sed -i -E "s/^\s+modules/& livestatus,webui/g" /etc/shinken/brokers/broker-master.cfg && \
            sed -i -E "s/^\s+modules/& auth-cfg-password, SQLitedb/g" /etc/shinken/modules/webui.cfg

# basic thruk config
COPY    thruk_local.conf /etc/thruk/thruk_local.conf
COPY    menu_local.conf /etc/thruk/menu_local.conf

# supervisor
RUN     pip install supervisor && \
            mkdir -p /etc/supervisord.d
COPY   apache.conf /etc/supervisord.d/apache.conf
COPY   crond.conf /etc/supervisord.d/crond.conf
COPY   snmpd.conf /etc/supervisord.d/snmpd.conf
COPY   ssh.conf /etc/supervisord.d/ssh.conf
COPY   thruk.supervisord.conf /etc/supervisord.d/thruk.conf
COPY   shinken.conf /etc/supervisord.d/shinken.conf
COPY   supervisord.conf /etc/supervisord.conf
COPY   startapache.sh /usr/local/bin/startapache.sh
RUN     chmod +x /usr/local/bin/startapache.sh

# patch livestatus module for contact notification period
COPY    mapping.py.contact.period.patch /var/lib/shinken/modules/livestatus/mapping.py.contact.period.patch
RUN     cd /var/lib/shinken/modules/livestatus && \
             patch < mapping.py.contact.period.patch

# sudo configuration 
COPY   sudoers.d.shinken /etc/sudoers.d/shinken
RUN     chmod 440 /etc/sudoers.d/shinken 

# fix config snmpd
RUN     echo "view   systemonly  included   .1" >> /etc/snmp/snmpd.conf

# default host config
COPY   shinken.cfg /etc/shinken/hosts/shinken.cfg
RUN     rm -f /etc/shinken/hosts/localhost.cfg

# permissions
RUN     chown -R www-data:www-data /etc/thruk/* && \
            chown -R shinken:shinken /var/lib/shinken /var/run/shinken && \
            usermod -a -G shinken www-data && \
            chown -R shinken:www-data /etc/shinken && \
            chmod -R g+rw /etc/shinken

# nagvis
RUN   cd /tmp && \
      apt-get -y install libapache2-mod-php5 php5-gd php-gettext php-net-socket php5-sqlite && \
      wget http://www.nagvis.org/share/nagvis-$NAGVISVERSION.tar.gz -O nagvis-$NAGVISVERSION.tar.gz && \
      tar zxvf nagvis-$NAGVISVERSION.tar.gz && \
      cd nagvis-$NAGVISVERSION && \
      ./install.sh -n /usr/sbin -a y -q -c n -r -o -F -u www-data -g www-data -w /etc/apache2/conf.d && \
      # sed -i "s/nagvis_session/PHPSESSID/g" /usr/local/nagvis/share/server/core/defines/global.php && \
      sed -i "s/^define('AUTH_PASSWORD_SALT.*$/define('AUTH_PASSWORD_SALT', '$NAGVISSALT');/g" /usr/local/nagvis/share/server/core/defines/global.php

COPY    nagvis.ini.php /usr/local/nagvis/etc/nagvis.ini.php
RUN     chown www-data:www-data /usr/local/nagvis/etc/nagvis.ini.php

CMD ["/usr/local/bin/supervisord", "-n", "-c", "/etc/supervisord.conf"]

