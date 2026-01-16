FROM debian:12-slim
LABEL Author="Rogger Fabri"

ARG ARCH=amd64
ARG GST_PLUGIN_SPOTIFY_VERSION_PATH=0.15.0-alpha.1-4
ARG GST_PLUGIN_SPOTIFY_VERSION_FILE=0.15.0.alpha.1-4

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1

RUN apt update && apt upgrade -y \
 && apt install -y \
    curl \
    dumb-init \
    libshout3 \
    mopidy \
    python3-pip \
    sudo \
 && mkdir -p ~/.config/pip && printf "[global]\nbreak-system-packages = true\n" | tee ~/.config/pip/pip.conf \
 && pip install \
    Mopidy-Iris \
    Mopidy-Local \
    Mopidy-Mobile \
    Mopidy-MPD \
    Mopidy-Scrobbler \
    Mopidy-Spotify==5.0.0a3 \
    Mopidy-TuneIn \
 && apt purge --auto-remove -y \
    gcc \
 && apt clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* ~/.cache /root/.cache

RUN curl -L -o gst-plugin-spotify_${GST_PLUGIN_SPOTIFY_VERSION_FILE}_${ARCH}.deb https://github.com/kingosticks/gst-plugins-rs-build/releases/download/gst-plugin-spotify_${GST_PLUGIN_SPOTIFY_VERSION_PATH}/gst-plugin-spotify_${GST_PLUGIN_SPOTIFY_VERSION_FILE}_${ARCH}.deb \
 && dpkg -i gst-plugin-spotify_${GST_PLUGIN_SPOTIFY_VERSION_FILE}_${ARCH}.deb \
  ; apt update && apt -f install -y \
 && rm gst-plugin-spotify_${GST_PLUGIN_SPOTIFY_VERSION_FILE}_${ARCH}.deb

RUN sh -c 'echo "mopidy ALL=NOPASSWD: /usr/local/lib/python3.11/dist-packages/mopidy_iris/system.sh" >> /etc/sudoers'

USER mopidy

EXPOSE 6600
EXPOSE 6680
EXPOSE 5555/udp

ADD ./start.sh /start.sh

ENTRYPOINT ["dumb-init", "--"]
CMD ["/start.sh"]

HEALTHCHECK --interval=60s --timeout=5s --retries=3 \
    CMD curl --connect-timeout 5 --silent --show-error --fail http://localhost:6680/ || exit 1
