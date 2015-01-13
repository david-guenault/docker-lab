# Shinken poller image
# VERSION    2.2

FROM                dguenault/shinken:2.2
MAINTAINER      David GUENAULT
ENV                  TAG 2.2-RC1

# snmp and nagios plugins
RUN     yum -y install nagios-plugins-all 

# manubulon plugins
RUN     wget http://nagios.manubulon.com/check_snmp_load.pl && \
            mv check_snmp_load.pl /usr/lib64/nagios/plugins && \
            chmod +x /usr/lib64/nagios/plugins/check_snmp_load.pl && \
            wget http://nagios.manubulon.com/check_snmp_storage.pl && \
            mv check_snmp_storage.pl /usr/lib64/nagios/plugins && \
            chmod +x /usr/lib64/nagios/plugins/check_snmp_storage.pl && \
            mkdir -p /usr/local/nagios && \
            ln -s /usr/lib64/nagios/plugins /usr/local/nagios/libexec && \
            wget http://nagios.manubulon.com/check_snmp_mem.pl && \
            mv check_snmp_mem.pl /usr/lib64/nagios/plugins && \
            chmod +x /usr/lib64/nagios/plugins/check_snmp_mem.pl && \
            wget http://nagios.manubulon.com/check_snmp_mem.pl && \
            mv check_snmp_mem.pl /usr/lib64/nagios/plugins && \
            chmod +x /usr/lib64/nagios/plugins/check_snmp_mem.pl && \
            wget http://nagios.manubulon.com/check_snmp_process.pl && \
            mv check_snmp_process.pl /usr/lib64/nagios/plugins && \
            chmod +x /usr/lib64/nagios/plugins/check_snmp_process.pl

# prerequisites for check_mywebsite
RUN     pip install docopt checkmyws-python

# packs and plugins
RUN     shinken --init && \
            shinken install mongodb && \
            shinken install check_mywebsite && \
            shinken install linux-ssh && \
            shinken install linux-snmp && \
            shinken install arbiter2 && \
            shinken install check_mywebsite && \
            pip install docopt checkmyws-python

# put check_netint.pl in nagios plugins folder
RUN     cp -a /var/lib/shinken/libexec/check_netint.pl /usr/lib64/nagios/plugins/ && \
            chmod +x /usr/lib64/nagios/plugins/

# fix user shinken to run nagios plugins
RUN     usermod -a -G nagios shinken

# daemon
ADD     files/supervisor/shinken.conf /etc/supervisord.d/

# port
EXPOSE 7771