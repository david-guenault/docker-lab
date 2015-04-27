FROM		debian:7
MAINTAINER 	David GUENAULT <david.guenault@gmail.com>

RUN     gpg --keyserver keys.gnupg.net --recv-keys F8C1CA08A57B9ED7 && \
            gpg --armor --export F8C1CA08A57B9ED7 | apt-key add - && \
            echo 'deb http://labs.consol.de/repo/stable/debian wheezy main' >> /etc/apt/sources.list && \
            apt-get update && \
            apt-get -y install apache2 python-pip thruk curl && \
            pip install supervisor && \
            /usr/local/bin/echo_supervisord_conf > /etc/supervisord.conf && \
            echo "[include]" >> /etc/supervisord.conf && \
            echo "files = supervisord.d/*.conf" >> /etc/supervisord.conf  

EXPOSE 80

ADD	files/supervisor/apache2.conf /etc/supervisord.d/

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisord.conf"]