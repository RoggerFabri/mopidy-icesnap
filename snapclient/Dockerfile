FROM debian:12-slim
LABEL Author="Rogger Fabri"

ENV DEBIAN_FRONTEND=noninteractive
ENV SERVER=snapserver
ENV DEVICE=Headphones
ENV CLIENT_ID=snapclient

ARG snapcast_version=0.34.0
ARG target_arch=arm64
ARG dist=bookworm

RUN apt update && apt upgrade -y \
    curl \
    dumb-init \
 && curl -sLO https://github.com/badaix/snapcast/releases/download/v${snapcast_version}/snapclient_${snapcast_version}-1_${target_arch}_${dist}.deb \
 && dpkg -i snapclient_${snapcast_version}-1_${target_arch}_${dist}.deb \
  ; apt update && apt -f install -y \
 && rm snapclient_${snapcast_version}-1_${target_arch}_${dist}.deb \
 && apt purge --auto-remove -y \
    gcc \
 && apt clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* ~/.cache /root/.cache

RUN /usr/bin/snapclient -v

ENTRYPOINT ["dumb-init", "--"]
CMD ["sh","-c","snapclient -h $SERVER -s $DEVICE --hostID $CLIENT_ID"]

HEALTHCHECK --interval=5s --timeout=3s \
   CMD pgrep snapclient || exit 1