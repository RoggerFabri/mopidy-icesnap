FROM debian:bullseye-20220316-slim
LABEL Author Rogger Fabri

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade -y \ 
 && apt install -y \
    curl \
    gnupg \
 && mkdir -p /usr/local/share/keyrings \
 && curl -sSL https://apt.mopidy.com/mopidy.gpg -o /usr/local/share/keyrings/mopidy-archive-keyring.gpg \
 && curl -sSL https://apt.mopidy.com/buster.list -o /etc/apt/sources.list.d/mopidy.list \
 && apt update \
 && apt install -y \
    mopidy \
    python3-pip \
    python3-spotify \
 && pip install \
    Mopidy-Iris \
    Mopidy-Local \
    Mopidy-Mobile \
    Mopidy-MPD \
    Mopidy-Scrobbler \
    Mopidy-Spotify \
    Mopidy-TuneIn \
 && apt purge --auto-remove -y \
    gcc \
 && apt clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* ~/.cache

COPY mopidy.sh /mopidy.sh

EXPOSE 6600
EXPOSE 6680
EXPOSE 5555/udp

ENTRYPOINT ["mopidy"]
CMD ["--config", "/mopidy/mopidy.conf"]

HEALTHCHECK --interval=60s --timeout=5s --retries=3 \
    CMD curl --connect-timeout 5 --silent --show-error --fail http://localhost:6680/ || exit 1
