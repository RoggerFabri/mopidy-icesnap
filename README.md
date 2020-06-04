# Mopidy with Icecast Docker Containers

## Setup

1. Clone this repo somewhere
2. Go to this link to get your Spotify authorisation details - [https://mopidy.com/ext/spotify/#authentication](https://mopidy.com/ext/spotify/#authentication)
3. Copy those details in to the relevant part of `mopidy/mopidy.conf`
4. Run `docker-compose up` in the root of the repo
5. Once you get the `Starting GLib mainloop` message, navigate to [http://localhost:6680/iris](http://localhost:6680/iris) to start using
6. Music will be streamed via Icecast at [http://localhost:8000/mopidy](http://localhost:8000/mopidy)

## Things to note

- This is using an experimental version of Mopidy-Iris, so will need to keep paths up to date
- Sometimes Iris will bug when first opened. Refresh for it to work again
