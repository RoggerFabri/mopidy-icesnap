FROM debian:12-slim
LABEL Author="Rogger Fabri"

ENV DEBIAN_FRONTEND=noninteractive

ARG raspotify_version=0.48.1
ARG target_arch=arm64

ENV DEVICE_NAME=Snapcast \
    BITRATE=320 \
    INITIAL_VOLUME=100 \
    ZEROCONF_PORT=39799 \
    ZEROCONF_BACKEND=avahi \
    CACHE_DIR=/var/cache/librespot \
    PIPE_PATH=/tmp/librespot-audio \
    METADATA_PIPE=/tmp/librespot-metadata \
    WATCHDOG_INTERVAL=30 \
    WATCHDOG_FAILURES=4 \
    LIBRESPOT_EXTRA_ARGS=

RUN apt update && apt upgrade -y \
    curl \
    dumb-init \
    jq \
 && RASPOTIFY_URL=$(curl -s https://api.github.com/repos/dtcooper/raspotify/releases/tags/${raspotify_version} | jq -r '.assets[] | select(.name | contains("raspotify") and contains("'${target_arch}'")) | .browser_download_url' | head -1) \
 && curl -sLO "${RASPOTIFY_URL}" \
 && dpkg -i raspotify_*_${target_arch}.deb \
  ; apt update && apt -f install -y \
 && rm raspotify_*_${target_arch}.deb \
 && apt clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* ~/.cache /root/.cache

RUN /usr/bin/librespot --version

COPY start.sh /start.sh
COPY onevent.sh /onevent.sh

EXPOSE 39799

ENTRYPOINT ["dumb-init", "--"]
CMD ["/start.sh"]

HEALTHCHECK --interval=60s --timeout=10s --start-period=120s --retries=3 \
    CMD curl --connect-timeout 5 --silent --show-error --fail "http://localhost:${ZEROCONF_PORT}/?action=getInfo" || exit 1
