# Shinken arbiter image
# VERSION    2.2

FROM                dguenault/shinken:2.2
MAINTAINER      David GUENAULT
ENV                  TAG 2.2-RC1

# snmp and nagios plugins
RUN     yum -y install python-whisper python-carbon pymongo pymongo-gridfs graphite-web

# supervisord
ADD         files/supervisor/shinken.conf /etc/supervisord.d/

# packs
RUN     shinken --init && \
            shinken install mongodb && \
            shinken install check_mywebsite && \
            shinken install arbiter2 && \
            shinken install linux-ssh && \
            shinken install linux-snmp && \
            pip install docopt checkmyws-python


# port
EXPOSE 7770
