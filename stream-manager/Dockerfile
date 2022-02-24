FROM alpine:latest
LABEL Author Rogger Fabri

ENV SNAPSERVER_IP=127.0.0.1
ENV SNAPSERVER_PORT=1780

ENV PIP_NO_CACHE_DIR=1

RUN apk update && apk upgrade \ 
 && apk add --no-cache \
    py3-pip \
    python3 \
 && pip3 install --upgrade pip \
 && pip3 install snapcast

COPY stream_manager.py stream_manager.py

CMD [ "python3","-u","./stream_manager.py" ]
