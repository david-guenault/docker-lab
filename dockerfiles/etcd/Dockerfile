# etcd in busybox
# VERSION 2.0.0-RC1


FROM        busybox 
MAINTAINER  David GUENAULT
ENV     TAG     2.0.0-rc1

ADD	files/${TAG}/etcd /
ADD	files/${TAG}/etcdctl /
RUN 	chmod +x /etcd /etcdctl

EXPOSE	4001
EXPOSE	7001

ENTRYPOINT [ "/etcd" ]
