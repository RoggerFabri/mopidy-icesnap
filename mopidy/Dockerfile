FROM debian:buster-slim

LABEL Author Rogger Fabri

RUN apt-get update \
       && DEBIAN_FRONTEND=noninteractive apt-get install -y --fix-missing \
       gcc \
       curl \
       python-crypto \
       python3-setuptools \
       python-pip \
       wget \
       git

RUN curl -L https://apt.mopidy.com/mopidy.gpg -o /tmp/mopidy.gpg \
       && wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/buster.list \
       && apt-key add /tmp/mopidy.gpg \
       && apt-get update \
       && apt-get install -y mopidy \
       && apt-get install -y mopidy-spotify \
       && apt-get install -y mopidy-mpd \
       && apt-get install -y mpc

RUN cd /tmp/ \
       && git clone --single-branch --branch develop https://github.com/jaedb/Iris.git \
       && cd Iris \
       && python3 setup.py install

RUN apt-get purge --auto-remove -y \
       curl \
       gcc \
       && apt-get clean \
       && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* ~/.cache

COPY mopidy.conf /var/lib/mopidy/.config/mopidy/mopidy.conf

USER mopidy

VOLUME /var/lib/mopidy

EXPOSE 6600
EXPOSE 6680

CMD ["/usr/bin/mopidy"]