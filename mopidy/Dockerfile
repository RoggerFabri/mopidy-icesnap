FROM debian:11-slim
LABEL Author Rogger Fabri

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade -y \ 
 && apt install -y \
    curl \
    gnupg \
 && rm -rf /var/lib/apt/lists/* \
 && curl -L https://apt.mopidy.com/mopidy.gpg | apt-key add - \
 && curl -L https://apt.mopidy.com/mopidy.list -o /etc/apt/sources.list.d/mopidy.list \
 && apt update \
 && apt install -y \
    build-essential \
    gir1.2-gst-plugins-base-1.0 \
    gir1.2-gstreamer-1.0 \
    gstreamer1.0-libav \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-tools \
    libffi-dev \
    libspotify-dev \
    libspotify12 \
    libxml2-dev \
    libxslt1-dev \
    libz-dev \
    python3-dev \
    python3-gst-1.0 \
    python3-pip \
    python3-setuptools \
    python3-spotify \
    python3-wheel \
    sudo \
    tzdata \
 && rm -rf /var/lib/apt/lists/* \
 && python3 -m pip install --upgrade pip \
 && pip install \
    Mopidy \
    Mopidy-Iris \
    Mopidy-Local \
    Mopidy-Mobile \
    Mopidy-MPD \
    Mopidy-Scrobbler \
    Mopidy-Spotify \
    Mopidy-TuneIn

COPY mopidy.sh /mopidy.sh
COPY mopidy_default.conf /mopidy_default.conf

EXPOSE 6600
EXPOSE 6680
EXPOSE 5555/udp

ENTRYPOINT ["/mopidy.sh"]

HEALTHCHECK --interval=60s --timeout=5s --retries=3 \
    CMD curl --connect-timeout 5 --silent --show-error --fail http://localhost:6680/ || exit 1
