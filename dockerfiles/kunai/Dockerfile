# kunai base image
# VERSION    latest

FROM                dguenault/kunai-base:latest
MAINTAINER      David GUENAULT

RUN     git clone https://github.com/naparuba/kunai.git && \
            cd kunai && \
            python setup.py install

EXPOSE 6768
EXPOSE 6769

ENTRYPOINT ["/usr/bin/kunai"]
