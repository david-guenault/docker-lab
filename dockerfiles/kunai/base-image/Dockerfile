# kunai base image
# VERSION    latest

FROM                debian:latest
MAINTAINER      David GUENAULT

# prerequisites
RUN      apt-get update && \
            apt-get -y install python-openssl python-setuptools python-pip python-leveldb git-core vim-nox telnet curl  gcc python-dev net-tools && \
            pip install requests cherrypy cherrypy-wsgiserver pycrypto

