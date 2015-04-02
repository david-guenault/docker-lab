# consul in debian/7
# VERSION 0.5.0


FROM        debian:wheezy
MAINTAINER  David GUENAULT
ENV     TAG     0.5.0

ADD ${TAG}_linux_amd64.zip /tmp/
ADD consul.cfg /etc/consul/consul.cfg
RUN apt-get update && \
        apt-get -y upgrade && \
        apt-get -y install unzip && \
        cd /tmp && \
        unzip ${TAG}_linux_amd64.zip && \
        mv consul /usr/bin/ && \
        rm -f consul  ${TAG}_linux_amd64.zip

ENTRYPOINT ["/usr/bin/consul"]

