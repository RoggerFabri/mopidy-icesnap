# Mopidy-IceSnap: Flexible Music Streaming Solution

A comprehensive Docker-based audio streaming solution offering two deployment options:

- **Mopidy with Icecast**: Network-wide audio streaming suitable for internet radio-like setups
- **Mopidy with Snapcast**: Synchronized multi-room audio streaming for whole-house sound systems

## What is Mopidy-IceSnap?

Mopidy-IceSnap combines multiple open-source technologies to create a flexible music streaming system that can be easily deployed using Docker. The project supports streaming from various music sources (Spotify, TuneIn, local files) and offers both synchronized and non-synchronized streaming options to meet different needs.

### Key Features

- **Two Flexible Setups**: Choose between Icecast (network streaming) or Snapcast (synchronized multi-room audio)
- **Beautiful Web Interface**: Control your music through the responsive Iris web interface
- **Multiple Music Sources**: Stream from Spotify, TuneIn, local files, and more
- **Multi-Platform Support**: Works on x86-64 and ARM64 architectures (including Raspberry Pi)
- **Docker-Based**: Easy deployment with containerized components
- **Automatic Stream Switching**: Seamlessly switch between different audio sources

---

## Use Cases

### Mopidy with Icecast

Perfect for:
- Creating your own internet radio station
- Streaming music to multiple devices across your network
- Making your music collection accessible from anywhere

This setup streams music through an Icecast server, making it accessible network-wide or even internet-wide if you expose your server (preferably behind a reverse proxy). While multiple clients can listen to the stream, the audio won't be synchronized between them.

### Mopidy with Snapcast

Ideal for:
- Multi-room home audio systems where perfect synchronization is important
- Creating a whole-house sound system
- Parties or events where the same music needs to play in multiple locations simultaneously

This setup enables perfectly synchronized audio across multiple rooms. Each room needs a client device (computer, Raspberry Pi, or even an old Android phone) connected to speakers.

---

## Components

### Mopidy

Mopidy is an extensible music server that plays music from various sources including:

- **Spotify**: Stream from Spotify's vast music library
- **TuneIn**: Access internet radio stations worldwide
- **Local Files**: Play your own music collection
- **MPD**: Compatible with numerous MPD clients
- **m3u Playlists**: Support for creating and playing playlists

The system uses Iris as the primary web frontend, offering a beautiful and responsive user interface for controlling your music.

### Snapcast

Snapcast provides multi-room client-server audio playback with perfect synchronization between all clients. Features include:

- **Time-Synchronized Playback**: All clients play audio in perfect sync
- **Multiple Stream Support**: Includes Mopidy and Spotify Connect streams
- **Various Client Options**: Desktop, mobile, and web clients available
- **Built-in Spotify Connect**: Stream directly from Spotify to Snapcast via Raspotify

### Stream Manager

A smart Python service that automatically manages active streams. When you:

1. Start playing music through Mopidy, all Snapcast clients receive that stream
2. Switch to playing through Spotify Connect, the Stream Manager automatically redirects all clients to the Spotify stream
3. Go back to Mopidy, clients automatically follow

This creates a seamless user experience without manual stream selection.

### Icecast

A reliable streaming server that makes your audio accessible across your network or the internet. Includes a basic web player page for easy listening.

---

## Getting Started

### Deployment Options

Choose the setup that best fits your needs:

1. **Mopidy with Icecast**: For network-wide streaming without synchronization
2. **Mopidy with Snapcast**: For synchronized multi-room audio

### Configuration

The Mopidy configuration for the Icecast setup is in `mopidy-icesnap/mopidy/mopidy-icecast.conf`. Important sections to configure:

- **[spotify]**: Add your `client_id` and `client_secret` from [Mopidy Spotify Authentication](https://mopidy.com/ext/spotify/#authentication)
- **[scrobbler]**: Optional Last.fm scrobbler configuration

For the Snapcast setup, review the `snapserver.conf` file and update Spotify credentials if needed.

### Access Points

- Mopidy-Iris web interface: `http://<your-server-ip>:6681`
- Icecast stream: `http://<your-server-ip>:8001`
- Snapcast web interface: `http://<your-server-ip>:1780`

You can customize ports via Docker Compose and use a reverse proxy like Caddy Server for HTTPS access.

### Client Setup

For the Snapcast multi-room setup, you'll need:
- A host device in each room running the `snapclient` Docker image or app
- Speakers connected to each client
- Optional: Android devices can run [Snapdroid](https://play.google.com/store/apps/details?id=de.badaix.snapcast) or use the web interface

## Docker Images

Pre-built Docker images are available at: [https://hub.docker.com/u/rfabri](https://hub.docker.com/u/rfabri)

### Supported Architectures

| Architecture | Available | Tag             |
| :----------: | :-------: | --------------- |
|    x86-64    |    ✅     | amd64-latest   |
|    arm64     |    ✅     | arm64v8-latest |

## Troubleshooting

### Common Issues

1. **No sound from Snapcast clients**
   - Check that the client is connected to the server
   - Verify audio devices are properly configured
   - Ensure firewall isn't blocking ports

2. **Spotify authentication fails**
   - Double-check client ID and secret
   - Verify Spotify account has an active subscription

3. **Icecast stream not accessible**
   - Check if the Icecast container is running
   - Verify port forwarding if accessing from outside the network

### Logs
Access container logs for troubleshooting:
```bash
docker logs mopidy
docker logs icecast
docker logs snapserver
```

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments
- [Mopidy](https://github.com/mopidy/mopidy) team for the excellent music server
- [Snapcast](https://github.com/badaix/snapcast) developers for the synchronized audio solution
- [Icecast](https://gitlab.xiph.org/xiph/icecast-server/) team for the streaming server
