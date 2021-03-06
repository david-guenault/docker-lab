FROM    dguenault/shinken-base:2.2
MAINTAINER David GUENAULT

ENV     DEBIAN_FRONTEND noninteractive

# upgrade
RUN      apt-get update && apt-get -y upgrade

# some prerequisites
RUN     apt-get install -y snmpd python-pip openssh-server sudo ssmtp

# Install thruk
RUN     gpg --keyserver keys.gnupg.net --recv-keys F8C1CA08A57B9ED7 && \
            gpg --armor --export F8C1CA08A57B9ED7 | apt-key add - && \
            echo 'deb http://labs.consol.de/repo/stable/debian wheezy main' >> /etc/apt/sources.list && \
            apt-get update && \
            apt-get -y --force-yes install thruk 

#openssh-server
RUN     mkdir /var/run/sshd && \
            echo "root:root" | chpasswd && \
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
COPY    thruk/thruk_local.conf /etc/thruk/thruk_local.conf
COPY    thruk/menu_local.conf /etc/thruk/menu_local.conf

# enable html output
RUN      sed -i -E "s/escape_html_tags=1/escape_html_tags=0/g" /etc/thruk/cgi.cfg

# supervisor
RUN     pip install supervisor && \
            mkdir -p /etc/supervisord.d
COPY   supervisor/apache.conf /etc/supervisord.d/apache.conf
COPY   supervisor/crond.conf /etc/supervisord.d/crond.conf
COPY   supervisor/snmpd.conf /etc/supervisord.d/snmpd.conf
COPY   supervisor/ssh.conf /etc/supervisord.d/ssh.conf
COPY   supervisor/thruk.conf /etc/supervisord.d/thruk.conf
COPY   supervisor/shinken.conf /etc/supervisord.d/shinken.conf
COPY   supervisor/supervisord.conf /etc/supervisord.conf
COPY   supervisor/rsyslog.conf /etc/supervisord.d/rsyslog.conf
COPY   supervisor/postfix.conf /etc/supervisord.d/postfix.conf

# patch livestatus module for contact notification period
COPY    mapping.py.contact.period.patch /var/lib/shinken/modules/livestatus/mapping.py.contact.period.patch
RUN     cd /var/lib/shinken/modules/livestatus && \
             patch < mapping.py.contact.period.patch

# sudo configuration 
COPY   sudo/shinken /etc/sudoers.d/shinken
RUN     chmod 440 /etc/sudoers.d/shinken 

# fix config snmpd
RUN     echo "view   systemonly  included   .1" >> /etc/snmp/snmpd.conf

# default host config
COPY   shinken-hosts/shinken.cfg /etc/shinken/hosts/shinken.cfg
RUN     rm -f /etc/shinken/hosts/localhost.cfg

# permissions
RUN     chown -R www-data:www-data /etc/thruk/* && \
            chown -R shinken:shinken /var/lib/shinken /var/run/shinken && \
            usermod -a -G shinken www-data && \
            usermod -a -G www-data shinken && \
            chown -R shinken:www-data /etc/shinken && \
            chmod -R g+rw /etc/shinken

# postfix for notifications in gmail (do not forget to create sasl_passwd file before building)
RUN      apt-get -y install rsyslog postfix mailutils libsasl2-2 ca-certificates libsasl2-modules vim-nox procps python-pip && \
            echo "postfix" > /etc/mailname

COPY    postfix/main.cf     /etc/postfix/main.cf
COPY    postfix/sasl_passwd /etc/postfix/sasl_passwd

RUN      postmap /etc/postfix/sasl_passwd && \
            chown postfix /etc/postfix/sasl_passwd* && \
            chmod 400 /etc/postfix/sasl_passwd

RUN     cat /etc/ssl/certs/Thawte_Premium_Server_CA.pem | tee -a /etc/postfix/cacert.pem

RUN      sed  -i -E "s/(\s+)?(modules.*$)/\1\2,graphite/g" /etc/shinken/brokers/broker-master.cfg

CMD ["/usr/local/bin/supervisord", "-n", "-c", "/etc/supervisord.conf"]

