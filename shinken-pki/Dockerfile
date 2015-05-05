FROM    debian:latest
MAINTAINER David GUENAULT

RUN     apt-get update 
RUN     apt-get -y install apache2
ADD     crl/signing-ca.crl /var/www/signing-ca.crl

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid

EXPOSE 80
ENTRYPOINT ["/usr/sbin/apache2", "-D", "FOREGROUND"]