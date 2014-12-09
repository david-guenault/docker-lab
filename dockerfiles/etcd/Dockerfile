# etcd in busybox
# VERSION 0.4.6	

FROM     	busybox	
MAINTAINER	David GUENAULT

ADD	files/etcd /
ADD	files/etcdctl /
RUN 	chmod +x /etcd /etcdctl

EXPOSE	4001
EXPOSE	7001

ENTRYPOINT [ "/etcd" ]
