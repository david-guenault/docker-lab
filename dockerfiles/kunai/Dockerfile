# kunai base image
# VERSION    latest

FROM                dguenault/kunai-base:latest
MAINTAINER      David GUENAULT

RUN     git clone https://github.com/naparuba/kunai.git && \
            cd kunai && \
            python setup.py install

# install supervisor and configuration 
# ADD     files/supervisor/supervisord.conf /etc/supervisord.conf 
# ADD     files/supervisor/kunai.conf /etc/supervisord.d/ 

