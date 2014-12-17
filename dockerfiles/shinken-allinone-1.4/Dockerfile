# Shinken All in One
# VERSION	1.4.4

FROM     	dguenault/shinken:1.4.4
MAINTAINER	David GUENAULT

# snmp and nagios plugins
RUN     yum -y install nagios-plugins-all && \
            yum -y install net-snmp net-snmp-utils perl-Net-SNMP pymongo pymongo-gridfs

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
            chmod +x /usr/lib64/nagios/plugins/check_snmp_mem.pl

# check_netint.pl
RUN     wget https://raw.githubusercontent.com/willixix/WL-NagiosPlugins/master/check_netint.pl && \
            mv check_netint.pl /usr/local/nagios/libexec && \ 
            chmod +x /usr/lib64/nagios/plugins/check_netint.pl

# little fix on linux pack
RUN     sed -i "s/-q -k -y/-q -k -y -g -2/g" /etc/shinken/packs/os/linux/commands.cfg

# fix snmpd configuration
RUN     sed -i "/^view/d" /etc/snmp/snmpd.conf
RUN     echo "view    systemview    included   .1" >> /etc/snmp/snmpd.conf

# daemons
ADD     files/supervisor/shinken.conf /etc/supervisord.d/
ADD     files/supervisor/snmpd.conf /etc/supervisord.d/

# Expose needed tcp ports
EXPOSE  7766
EXPOSE  7767
EXPOSE  7768
EXPOSE  7769
EXPOSE  7770
EXPOSE  7771
EXPOSE  7772

