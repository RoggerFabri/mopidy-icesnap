FROM alpine:latest
LABEL Author Rogger Fabri

RUN apk update && apk upgrade \ 
 && apk add \
    python3 \
    py3-pip \
 && pip3 install --upgrade pip \
 && pip3 install snapcast

COPY stream_manager.py stream_manager.py

CMD [ "python3","-u","./stream_manager.py" ]
