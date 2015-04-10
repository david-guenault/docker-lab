FROM centos:6.6
MAINTAINER David GUENAULT

COPY shinken-enterprise-2.03-update.tar.gz /tmp/
COPY user.key /tmp/

RUN     yum -y install tar gunzip && \
            cd /tmp && \
            tar zxvf shinken-enterprise-2.03-update.tar.gz && \
            cd shinken-enterprise-2.03-update && \
            yum -y install https://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm && \
            yum -y localinstall shinken-enterprise-2.03-update.tar.gz && \
            rm -Rf /tmp/shinken-enterprise-2.03-update




