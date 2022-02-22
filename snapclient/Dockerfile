FROM debian:bullseye-slim
LABEL Author Rogger Fabri

ENV DEBIAN_FRONTEND=noninteractive
ENV SERVER snapserver
ENV DEVICE Headphones
ENV CLIENT_ID snapclient

ARG snapcast_version=0.26.0
ARG target_arch=armhf

RUN apt update && apt upgrade -y \
 && apt install -y \
    curl \
 && curl -sLO https://github.com/badaix/snapcast/releases/download/v${snapcast_version}/snapclient_${snapcast_version}-1_${target_arch}.deb \
 && dpkg -i snapclient_${snapcast_version}-1_${target_arch}.deb \
 ;  apt update \
 && apt -f install -y \
 && rm -rf /var/lib/apt/lists/* \
 && /usr/bin/snapclient -v

ENTRYPOINT ["/bin/bash","-c","/usr/bin/snapclient -h $SERVER -s $DEVICE --hostID $CLIENT_ID"]
