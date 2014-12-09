# Shinken from master branch 
# VERSION	2.2

FROM     centos:centos6
MAINTAINER	David GUENAULT

# install repo
RUN     yum -y install http://mirrors.ircam.fr/pub/fedora/epel/6/i386/epel-release-6-8.noarch.rpm
RUN	rpm --import http://packages.elasticsearch.org/GPG-KEY-elasticsearch
RUN 	yum clean all
ADD	files/repos/elasticsearch.repo /etc/yum.repos.d/
ADD	files/repos/logstash.repo /etc/yum.repos.d/

# prerequisites
RUN     yum -y install vim-enhanced httpd elasticsearch java-1.7.0-openjdk python-pip redis logstash wget tar

# install supervisor and configuration 
RUN     pip install supervisor
RUN     mkdir -p /etc/supervisord.d
RUN     mkdir -p /var/log/supervisord
ADD     files/supervisor/supervisord.conf /etc/supervisord.conf
ADD     files/supervisor/logstash.conf /etc/supervisord.d/
ADD     files/supervisor/redis.conf /etc/supervisord.d/
ADD     files/supervisor/elasticsearch.conf /etc/supervisord.d/
ADD     files/supervisor/httpd.conf /etc/supervisord.d/

# redis
RUN	sed -i "s/^\(bind.*\)/#\1/g" /etc/redis.conf
RUN	sed -i "s/^\(daemonize\) \(.*\)/\1 no/g" /etc/redis.conf

# logstash
ADD	files/logstash/logstash.conf /etc/logstash/

# elasticsearch 
RUN	sed -i "s/^#cluster\.name.*/cluster\.name: elk/g" /etc/elasticsearch/elasticsearch.yml
RUN	sed -i "s/^#node\.name.*/node.name: \"node1\"/g" /etc/elasticsearch/elasticsearch.yml

# elastichq
RUN	cd /usr/share/elasticsearch/bin && ./plugin -install royrusso/elasticsearch-HQ

# kibana 
RUN 	wget https://download.elasticsearch.org/kibana/kibana/kibana-3.1.2.tar.gz
RUN	tar zxvf kibana-3.1.2.tar.gz
RUN	mv kibana-3.1.2 /var/www/html/kibana	
RUN	chown -R apache:apache /var/www/html/kibana
RUN	sed -i "s/^\(apache.*:\)\(\/sbin\/nologin\)/\1\/bin\/bash/g" /etc/passwd
# Expose needed tcp ports

EXPOSE  9200
EXPOSE  9300
EXPOSE  6379
EXPOSE  80



CMD ["supervisord", "-c", "/etc/supervisord.conf", "-n"]
