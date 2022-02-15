FROM debian:bullseye-slim
LABEL Author Rogger Fabri

ENV DEBIAN_FRONTEND=noninteractive

ARG snapcast_version=0.26.0
ARG target_arch=armhf

ENV SERVER snapserver
ENV DEVICE Headphones
ENV CLIENT_ID snapclient

RUN apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    gnupg \
    curl
  
RUN wget https://github.com/badaix/snapcast/releases/download/v${snapcast_version}/snapclient_${snapcast_version}-1_${target_arch}.deb
RUN dpkg -i snapclient_${snapcast_version}-1_${target_arch}.deb \
  ;  apt-get update \
  && apt-get -f install -y

RUN rm -rf /var/lib/apt/lists/*

RUN /usr/bin/snapclient -v
ENTRYPOINT ["/bin/bash","-c","/usr/bin/snapclient -h $SERVER -s $DEVICE --hostID $CLIENT_ID"]
