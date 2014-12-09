# Docker file for skydns 2 build from source 
# VERSION 2

FROM     	centos:centos6
MAINTAINER	David GUENAULT

# epel
RUN     yum -y install http://mirrors.ircam.fr/pub/fedora/epel/6/i386/epel-release-6-8.noarch.rpm && \
	yum clean all

# prerequisites
RUN     yum -y install hg golang tar 

# git 1.9 ... because epel version does not work with go ....
RUN 	yum -y install curl-devel expat-devel gettext-devel openssl-devel zlib-devel gcc perl-ExtUtils-MakeMaker wget 
RUN	cd /usr/src 
RUN	wget https://www.kernel.org/pub/software/scm/git/git-1.9.4.tar.gz 
RUN	tar xzf git-1.9.4.tar.gz 
RUN	cd git-1.9.4 && \
	make prefix=/usr/local/git all && \
	make prefix=/usr/local/git install && \
	ln -s /usr/local/git/bin/git /usr/bin/git


# install skydns
RUN	mkdir -p /gocode && \
	export GOPATH=/gocode && \ 
	go get github.com/skynetservices/skydns 

