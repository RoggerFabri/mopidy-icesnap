FROM python:3.11.0a5-bullseye
LABEL Author Rogger Fabri

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1

ARG snapcast_version=0.26.0
ARG target_arch=armhf

RUN apt update && apt upgrade -y \
    build-essential \
    curl \
    libdbus-glib-1-dev \
    libgirepository1.0-dev \
 && python -m pip install --upgrade pip \
 && pip install python-mpd2 musicbrainzngs pydbus PyGObject dbus-python \
 && curl -sLO https://github.com/badaix/snapcast/releases/download/v${snapcast_version}/snapserver_${snapcast_version}-1_${target_arch}.deb \
 && dpkg -i snapserver_${snapcast_version}-1_${target_arch}.deb \
  ; apt update && apt -f install -y \
 && rm snapserver_${snapcast_version}-1_${target_arch}.deb \
 && curl -sSL https://dtcooper.github.io/raspotify/key.asc | tee /usr/share/keyrings/raspotify_key.asc  > /dev/null \
 && chmod 644 /usr/share/keyrings/raspotify_key.asc \
 && echo 'deb [signed-by=/usr/share/keyrings/raspotify_key.asc] https://dtcooper.github.io/raspotify raspotify main' | tee /etc/apt/sources.list.d/raspotify.list \
 && apt update && apt -y install \
    raspotify \
 && apt purge --auto-remove -y \
    gcc \
 && apt clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* ~/.cache /root/.cache

RUN /usr/bin/snapserver -v

COPY www/ /www/

EXPOSE 1704 1705 1780

ENTRYPOINT ["/bin/bash","-c","/usr/bin/snapserver"]

HEALTHCHECK --interval=60s --timeout=5s --retries=3 \
    CMD curl --connect-timeout 5 --silent --show-error --fail http://localhost:1780/ || exit 1
