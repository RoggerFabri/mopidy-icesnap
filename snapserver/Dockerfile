FROM debian:buster-slim
LABEL Author Rogger Fabri

ENV DEBIAN_FRONTEND=noninteractive

ARG snapcast_version=0.20.0
ARG target_arch=armhf

ARG SPOTIFY_USERNAME
ARG SPOTIFY_PASSWORD

RUN apt-get update && \
    apt-get install -y wget ca-certificates gnupg

RUN wget https://github.com/badaix/snapcast/releases/download/v${snapcast_version}/snapserver_${snapcast_version}-1_${target_arch}.deb
RUN dpkg -i snapserver_${snapcast_version}-1_${target_arch}.deb \
  ;  apt-get update \
  && apt-get -f install -y

RUN wget --no-check-certificate -qO - https://dtcooper.github.io/raspotify/key.asc | apt-key add -
RUN echo 'deb https://dtcooper.github.io/raspotify raspotify main' | tee /etc/apt/sources.list.d/raspotify.list

RUN apt-get update
RUN apt-get -y install raspotify

RUN /usr/bin/snapserver -v
COPY snapserver.conf /etc/snapserver.conf

RUN sed -i "s/SPOTIFY_USERNAME/${SPOTIFY_USERNAME}/g" /etc/snapserver.conf
RUN sed -i "s/SPOTIFY_PASSWORD/${SPOTIFY_PASSWORD}/g" /etc/snapserver.conf

COPY www/* /www/

ENTRYPOINT ["/bin/bash","-c","/usr/bin/snapserver"]