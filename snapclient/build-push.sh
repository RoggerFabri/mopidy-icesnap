#!/bin/bash

docker build --build-arg TARGETARCH=arm --no-cache -t rfabri/snapclient:latest .
docker push rfabri/snapclient:latest