FROM alpine:latest
LABEL Author Rogger Fabri

ENV SERVER=snapserver
ENV DEVICE=Headphones
ENV CLIENT_ID=snapclient

RUN apk update && apk upgrade \ 
 && apk add --no-cache \
    snapcast

CMD ["sh","-c","snapclient -h $SERVER -s $DEVICE --hostID $CLIENT_ID"]
