# Mopidy with Icecast and Snapcast Docker Containers

## Setup

### TODO

Authentication: https://mopidy.com/ext/spotify/#authentication

Mopidy
- Iris (frontend)
- Mobile (frontend)
- TuneIn
- MPD
- Local
- m3u
- Spotify

Snapcast
- Streams
    - [Mopidy] TCP stream using `tcpclientsink` instead of fifo `tmp/snapfifo`
    - [Spotify] Spotify Connect stream from `librespot`

Icecast

- SnapDotNet
- SnapDroid
- MPDCtrl for desktop