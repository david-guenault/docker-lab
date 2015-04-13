FROM    dguenault/shinken-base:2.2
MAINTAINER David GUENAULT

ENV     DEBIAN_FRONTEND noninteractive
ENV     NAGVISVERSION 1.8.2
ENV     NAGVISSALT 29d58ead6a65f5c00342ae03cdc6d26565e20954

# upgrade
RUN      apt-get update && apt-get -y upgrade && apt-get -y install openssh-server

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

# supervisor
RUN     pip install supervisor && \
            mkdir -p /etc/supervisord.d
COPY   supervisor/apache.conf /etc/supervisord.d/apache.conf
COPY   supervisor/sshd.conf /etc/supervisord.d/sshd.conf
COPY   supervisor/supervisord.conf /etc/supervisord.conf

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
