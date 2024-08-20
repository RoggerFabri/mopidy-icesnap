FROM debian:12-slim
LABEL Author="Rogger Fabri"

ARG ARCH=amd64

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1

RUN apt update && apt upgrade -y \
 && apt install -y \
    curl \
    dumb-init \
    mopidy \
    python3-pip \
 && mkdir -p ~/.config/pip && printf "[global]\nbreak-system-packages = true\n" | tee ~/.config/pip/pip.conf \
 && pip install \
    Mopidy-Iris \
    Mopidy-Local \
    Mopidy-Mobile \
    Mopidy-MPD \
    Mopidy-Scrobbler \
    Mopidy-Spotify==5.0.0a2 \
    Mopidy-TuneIn \
 && apt purge --auto-remove -y \
    gcc \
 && apt clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* ~/.cache /root/.cache

RUN curl -L -o gst-plugin-spotify_0.12.2-1_${ARCH}.deb https://github.com/kingosticks/gst-plugins-rs-build/releases/download/gst-plugin-spotify_0.12.2-1/gst-plugin-spotify_0.12.2-1_${ARCH}.deb \
 && dpkg -i gst-plugin-spotify_0.12.2-1_${ARCH}.deb \
  ; apt update && apt -f install -y

RUN curl -L -o libshout3_2.4.1-2_${ARCH}.deb http://ftp.de.debian.org/debian/pool/main/libs/libshout/libshout3_2.4.1-2_${ARCH}.deb \
 && dpkg -i libshout3_2.4.1-2_${ARCH}.deb \
 ; apt update && apt -f install -y

EXPOSE 6600
EXPOSE 6680
EXPOSE 5555/udp

ADD ./start.sh /start.sh

ENTRYPOINT ["dumb-init", "--"]
CMD ["/start.sh"]

HEALTHCHECK --interval=60s --timeout=5s --retries=3 \
    CMD curl --connect-timeout 5 --silent --show-error --fail http://localhost:6680/ || exit 1
