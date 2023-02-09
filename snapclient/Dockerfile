FROM alpine:3.17
LABEL Author="Rogger Fabri"

ENV SERVER=snapserver
ENV DEVICE=Headphones
ENV CLIENT_ID=snapclient

RUN apk update && apk upgrade \
 && apk add --no-cache \
    snapcast \
    tzdata \
 && rm -rf /var/cache/apk/* /root/.cache

CMD ["sh","-c","snapclient -h $SERVER -s $DEVICE --hostID $CLIENT_ID"]
