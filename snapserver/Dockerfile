FROM debian:12-slim
LABEL Author="Rogger Fabri"

ENV DEBIAN_FRONTEND=noninteractive

ARG snapcast_version=0.32.2
ARG target_arch=arm64
ARG dist=bookworm

RUN apt update && apt upgrade -y \
    curl \
    dumb-init \
 && curl -sLO https://github.com/badaix/snapcast/releases/download/v${snapcast_version}/snapserver_${snapcast_version}-1_${target_arch}_${dist}.deb \
 && dpkg -i snapserver_${snapcast_version}-1_${target_arch}_${dist}.deb \
  ; apt update && apt -f install -y \
 && rm snapserver_${snapcast_version}-1_${target_arch}_${dist}.deb \
 && curl -sL https://dtcooper.github.io/raspotify/install.sh | sh \
 && apt purge --auto-remove -y \
    gcc \
 && apt clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* ~/.cache /root/.cache

RUN /usr/bin/snapserver -v

EXPOSE 1704 1705 1780

ENTRYPOINT ["dumb-init", "--"]
CMD ["bash","-c","snapserver"]

HEALTHCHECK --interval=60s --timeout=5s --retries=3 \
    CMD curl --connect-timeout 5 --silent --show-error --fail http://localhost:1780/ || exit 1
