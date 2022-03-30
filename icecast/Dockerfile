FROM debian:11-slim
LABEL Author Rogger Fabri

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade -y \ 
 && apt install -y \
    icecast2 \
    sudo \
 && rm -rf /usr/share/icecast2/web/* \
 && apt clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* ~/.cache /root/.cache

COPY icecast.xml /etc/icecast2/icecast.xml
COPY silence.mp3 /usr/share/icecast2/web/silence.mp3
COPY www/ /usr/share/icecast2/web/

RUN chown -R icecast2 /usr/share/icecast2

VOLUME ["/var/log/icecast2", "/usr/share/icecast2"]

ADD ./start.sh /start.sh

EXPOSE 8000

CMD ["/start.sh"]
