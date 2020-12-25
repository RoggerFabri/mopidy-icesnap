FROM debian:buster-slim

ARG snapcast_version=0.22.0
ARG TARGETARCH
ENV HOST snapserver
ENV DEVICE Headphones

RUN  apt-get update \
  && apt-get install -y wget ca-certificates \
  && rm -rf /var/lib/apt/lists/*
  
RUN  wget https://github.com/badaix/snapcast/releases/download/v${snapcast_version}/snapclient_${snapcast_version}-1_$(echo $TARGETARCH | sed 's/arm/armhf/g').deb
RUN  dpkg -i snapclient_${snapcast_version}-1_$(echo $TARGETARCH | sed 's/arm/armhf/g').deb \
  ;  apt-get update \
  && apt-get -f install -y \
  && rm -rf /var/lib/apt/lists/*
RUN /usr/bin/snapclient -v
ENTRYPOINT ["/bin/bash","-c","/usr/bin/snapclient -h $HOST -s $DEVICE"]