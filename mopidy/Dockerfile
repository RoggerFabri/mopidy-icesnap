FROM debian:11-slim
LABEL Author="Rogger Fabri"

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1

RUN apt update && apt upgrade -y \
 && apt install -y \
    curl \
    dumb-init \
    mopidy \
    python3-pip \
 && pip install \
    Mopidy-Iris \
    Mopidy-Local \
    Mopidy-Mobile \
    Mopidy-MPD \
    Mopidy-Scrobbler \
  # Mopidy-Spotify \
    Mopidy-TuneIn \
 && apt purge --auto-remove -y \
    gcc \
 && apt clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* ~/.cache /root/.cache

EXPOSE 6600
EXPOSE 6680
EXPOSE 5555/udp

ADD ./start.sh /start.sh

ENTRYPOINT ["dumb-init", "--"]
CMD ["/start.sh"]

HEALTHCHECK --interval=60s --timeout=5s --retries=3 \
    CMD curl --connect-timeout 5 --silent --show-error --fail http://localhost:6680/ || exit 1
