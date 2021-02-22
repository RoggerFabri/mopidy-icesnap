# Mopidy with Icecast / Snapcast on Docker containers

This repository contains two setups:

- [Mopidy](https://github.com/mopidy/mopidy) with audio streaming across a network using [Icecast](https://gitlab.xiph.org/xiph/icecast-server/);
- [Mopidy](https://github.com/mopidy/mopidy) with synchronized multi-room audio streaming using [Snapcast](https://github.com/badaix/snapcast);

Mopidy is a music server and handles streaming services such as TuneIn, Spotify, Local Files and is extensible to other services. [Iris](https://github.com/jaedb/Iris) is the frontend extension chosen for Mopidy because is responsive, user-friendly and beautifully designed.

---

## Mopidy with Icecast

This setup streams music from a chosen source and stream it via an Icecast Server, making the stream accessible network wide or internet wide should you want to expose your server. Icecast doesn't synchronize the listeners/clients so, although this setup can be used to a multi-room scenario, it won't deliver the perfect setup. I use it to stream music for my private internet radio.

In this setup, Mopidy-Iris is controlled at: `http://<your-server-ip>:6681` and Icecast is streamed at: `http://<your-server-ip>:8001`. The Icecast container comes with a basic webpage with an audio player to play whatever Mopidy is streaming. See the `icecast/www` folder for details. 

### Configuration

The Mopidy configuration for this setup is fetched from the folder `mopidy-icesnap/mopidy/mopidy-icecast.conf`. The output doesn't need to be changed. Important sections here are:

- [spotify] - Authenticate here https://mopidy.com/ext/spotify/#authentication and paste in the `client_id` and `client_secret`;
- [scrobbler] - Last.fm scrobbler if you want to enable it, not mandatory;
- [youtube] - Allows streaming audio from Youtube videos, not mandatory;

---

## Mopidy with Snapcast

`TODO`

## Mopidy

`TODO`

- Iris (frontend)
- Mobile (frontend)
- TuneIn
- MPD
- Local
- m3u
- Spotify

## Snapcast

`TODO`

- Streams
    - [Mopidy] FIFO stream using `tmp/snapfifo`
    - [Spotify] Spotify Connect stream from `librespot` (Raspotify)

- Clients
    - SnapDotNet
    - SnapDroid
    - MPDCtrl for desktop

## Stream Manager

`TODO`

## Icecast

`TODO`

## Raspberry Pi Docker Images

Raspberry Pi images can be found at:

https://hub.docker.com/u/rfabri

I try to update the images whenever there's a new release for the used componentes. At the moment I'm maintaining images for:

- snapclient
- mopidy
- snapserver
