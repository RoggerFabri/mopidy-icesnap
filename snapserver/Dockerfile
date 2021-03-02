FROM debian:buster-slim
LABEL Author Rogger Fabri

ENV DEBIAN_FRONTEND=noninteractive

ARG snapcast_version=0.24.0
ARG target_arch=armhf

RUN apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    gnupg

RUN wget https://github.com/badaix/snapcast/releases/download/v${snapcast_version}/snapserver_${snapcast_version}-1_${target_arch}.deb
RUN dpkg -i snapserver_${snapcast_version}-1_${target_arch}.deb \
  ;  apt-get update \
  && apt-get -f install -y

RUN wget --no-check-certificate -qO - https://dtcooper.github.io/raspotify/key.asc | apt-key add -
RUN echo 'deb https://dtcooper.github.io/raspotify raspotify main' | tee /etc/apt/sources.list.d/raspotify.list

RUN apt-get update && apt-get -y install \
    raspotify \
    && rm -rf /var/lib/apt/lists/*

RUN /usr/bin/snapserver -v

COPY www/ /www/

EXPOSE 1704 1705 1780

ENTRYPOINT ["/bin/bash","-c","/usr/bin/snapserver"]