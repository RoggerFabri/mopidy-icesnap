FROM alpine:3.16
LABEL Author="Rogger Fabri"

ENV SNAPSERVER_IP=127.0.0.1
ENV SNAPSERVER_PORT=1780
ENV PIP_NO_CACHE_DIR=1

RUN apk update && apk upgrade \
 && apk add --no-cache \
    py3-pip \
    python3 \
    tzdata \
 && pip3 install --upgrade pip \
 && pip3 install apscheduler \
 && pip3 install snapcast \
 && rm -rf /var/cache/apk/* /root/.cache 

COPY stream_manager.py stream_manager.py

CMD [ "python3","-u","./stream_manager.py" ]
