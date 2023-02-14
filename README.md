# Mopidy with Icecast / Snapcast on Docker Containers

This repository contains two setups:

- [Mopidy](https://github.com/mopidy/mopidy) with audio streaming across a network using [Icecast](https://gitlab.xiph.org/xiph/icecast-server/);
- [Mopidy](https://github.com/mopidy/mopidy) with synchronized multi-room audio streaming using [Snapcast](https://github.com/badaix/snapcast);

Mopidy is a music server and handles streaming services such as TuneIn, Spotify, Local Files and is extensible to other services. [Iris](https://github.com/jaedb/Iris) is the frontend extension chosen for Mopidy because is responsive, user-friendly and beautifully designed.

---

## Mopidy with Icecast

This setup streams music from a chosen source and stream it via an Icecast Server, making the stream accessible network wide or internet wide in case you want to expose your server, behind a reverse proxy, for example. Icecast doesn't synchronize the listeners/clients so, although this setup can be used to a multi-room scenario, it won't deliver the perfect experience (Mopidy with Snapcast is made for that). A good use is to stream music for an internet radio.

In this setup, Mopidy-Iris is controlled at: `http://<your-server-ip>:6681` and Icecast is streamed at: `http://<your-server-ip>:8001`. The Icecast container comes with a basic webpage with an audio player to play whatever Mopidy is streaming. See the `icecast/www` folder for details. Of course the ports can be customized on demand via `docker-compose` and you can expose your service through HTTPS using a reverse proxy. In my local network I'm using Caddy Server <https://hub.docker.com/_/caddy> as my reverse proxy solution to serve my services in HTTPS.

### Configuration

The Mopidy configuration for this setup is fetched from the folder `mopidy-icesnap/mopidy/mopidy-icecast.conf`. The output doesn't need to be changed. Important sections here are:

- [spotify] - Authenticate here <https://mopidy.com/ext/spotify/#authentication> and paste in the `client_id` and `client_secret`;
- [scrobbler] - Last.fm scrobbler if you want to enable it, not mandatory;

---

## Mopidy with Snapcast

This setup is perfect for a multi-room audio where the clients are synchronized to each other. As well the streaming can be controlled from a single source (Mopidy), while being accessible from various devices on a fantastic web client. The setup consists of a main streaming server with several clients in each room, for each room you'll need a host capable of running the `snapclient` docker image or, alternatively, you can use an old Android phone either installing Snapcast (<https://play.google.com/store/apps/details?id=de.badaix.snapcast>) or using the web interface from your Snapcast server. You'll also need one speaker for each client (oh really?).
Once connected to the server, clients automatically syncronize the streaming.

## Mopidy

Mopidy is a music server with support for MPD clients and HTTP clients.

Includes the following extensions:

- Iris (frontend)
- Mobile (frontend)
- TuneIn
- MPD
- Local
- m3u
- Spotify

## Snapcast

Snapcast is a multiroom client-server audio player, where all clients are time synchronized with the server to play perfectly synced audio. This version comes with [Raspotify](https://github.com/dtcooper/raspotify) baked in.

- Streams
  - [Mopidy] FIFO stream using `tmp/snapfifo`
  - [Spotify] Spotify Connect stream from `librespot` (Raspotify)

- Clients
  - [Snap.Net](https://github.com/stijnvdb88/Snap.Net)
  - [snapdroid](https://github.com/badaix/snapdroid)
  - [MPDCtrl](https://github.com/torum/MPDCtrl)

## Stream Manager

A simple python script that automatically switches to the active streaming queue on Snapserver. It's a simple automation to make a seamless streaming whenever you want to switch from Spotify Connect (Raspotify) to Mopidy and vice-versa without the hassle of choosing the streaming queues.

## Icecast

Icecast is a server — an audio streaming server to be precise.

## Docker Images

Docker images can be found at:

<https://hub.docker.com/u/rfabri>

### Supported Architectures

The architectures supported by the images on this repository are:

| Architecture | Available | Tag             |
| :----------: | :-------: | --------------- |
|    x86-64    |    ✅     | amd64-latest   |
|    arm64     |    ✅     | arm64v8-latest |
