# Shinken from master branch 
# VERSION	2.0.3

FROM     	debian:latest
MAINTAINER	David GUENAULT

RUN	mkdir -p /usr/sbin
ADD	files/skydns /usr/sbin/
RUN	chmod +x /usr/sbin/skydns

EXPOSE 53

ENTRYPOINT [ "/usr/sbin/skydns" ]

