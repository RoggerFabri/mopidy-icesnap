FROM alpine:3.17
LABEL Author="Rogger Fabri"

ENV SERVER=snapserver
ENV DEVICE=Headphones
ENV CLIENT_ID=snapclient

RUN apk update && apk upgrade \
 && apk add --no-cache \
    dumb-init \
    snapcast \
    tzdata \
 && rm -rf /var/cache/apk/* /root/.cache

ENTRYPOINT ["dumb-init", "--"]
CMD ["sh","-c","snapclient -h $SERVER -s $DEVICE --hostID $CLIENT_ID"]

HEALTHCHECK --interval=5s --timeout=3s \
   CMD pgrep snapclient || exit 1
