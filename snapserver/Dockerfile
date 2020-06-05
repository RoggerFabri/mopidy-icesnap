FROM debian:buster-slim
LABEL Author Rogger Fabri

ENV DEBIAN_FRONTEND=noninteractive

ARG snapcast_version=0.19.0
ARG target_arch=armhf

RUN apt-get update \
  && apt-get install -y wget ca-certificates \
  && rm -rf /var/lib/apt/lists/*
RUN wget https://github.com/badaix/snapcast/releases/download/v${snapcast_version}/snapserver_${snapcast_version}-1_${target_arch}.deb
RUN dpkg -i snapserver_${snapcast_version}-1_${target_arch}.deb \
  ;  apt-get update \
  && apt-get -f install -y \
  && rm -rf /var/lib/apt/lists/*

RUN /usr/bin/snapserver -v
COPY snapserver.conf /etc/snapserver.conf
COPY www/* /www/

EXPOSE 1704
EXPOSE 1705
EXPOSE 1780
EXPOSE 4953

ENTRYPOINT ["/bin/bash","-c","/usr/bin/snapserver"]