FROM debian:bullseye-20211011-slim
LABEL Author Rogger Fabri

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    ca-certificates \
    gnupg && \
    rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://apt.mopidy.com/mopidy.gpg | apt-key add - && \
    wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/buster.list

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tzdata \
    sudo \
    build-essential \
    python3-dev \
    python3-pip \
    python3-gst-1.0 \
    python3-wheel \
    gir1.2-gstreamer-1.0 \
    gir1.2-gst-plugins-base-1.0 \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-libav \
    gstreamer1.0-tools \
    libspotify12 \
    libspotify-dev \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    libz-dev \
    curl \
    python3-setuptools \
    python3-spotify && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install \
    Mopidy \
    Mopidy-MPD \
    Mopidy-Local \
    Mopidy-TuneIn \
    Mopidy-Spotify \
    Mopidy-Mobile \
    Mopidy-Iris \
    Mopidy-Scrobbler

COPY mopidy.sh /mopidy.sh
COPY mopidy_default.conf /mopidy_default.conf

EXPOSE 6600
EXPOSE 6680
EXPOSE 5555/udp

ENTRYPOINT ["/mopidy.sh"]

HEALTHCHECK --interval=60s --timeout=5s --retries=3 \
    CMD curl --connect-timeout 5 --silent --show-error --fail http://localhost:6680/ || exit 1
