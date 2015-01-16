# Shinken receiver image
# VERSION    2.2

FROM                dguenault/shinken:2.2
MAINTAINER      David GUENAULT
ENV                  TAG 2.2-RC1

# daemon
ADD     files/supervisor/shinken.conf /etc/supervisord.d/

# port
EXPOSE 7773