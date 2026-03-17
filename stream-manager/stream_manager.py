import asyncio
import logging
import os
import snapcast.control
import sys
from typing import Optional

# Configure logging
logging.basicConfig(
    format='[%(asctime)s] %(levelname)-8s [%(funcName)s:%(lineno)d] — %(message)s',
    level=logging.INFO,
    datefmt='%d-%m-%Y %H:%M:%S')

# Reduce noise from apscheduler
logging.getLogger('apscheduler').setLevel(logging.ERROR)

# Get configuration from environment variables with defaults
serverIp = os.environ.get('SNAPSERVER_IP')
serverPort = os.environ.get('SNAPSERVER_PORT')
reconnect_interval = int(os.environ.get('RECONNECT_INTERVAL', '60'))

logging.info(f'SNAPSERVER_IP: {serverIp}')
logging.info(f'SNAPSERVER_PORT: {serverPort}')

# Validate required configuration
if serverIp is None:
    logging.error('ENV|SNAPSERVER_IP not provided, exiting...')
    sys.exit(1)
if serverPort is None:
    logging.error('ENV|SNAPSERVER_PORT not provided, exiting...')
    sys.exit(1)

server: Optional[snapcast.control.server] = None

async def connect_to_server(ip: str, port: str) -> snapcast.control.server:
    """Establish connection to the Snapcast server."""
    while True:
        try:
            logging.info(f'Connecting to server at {ip}:{port}...')
            srv = await snapcast.control.create_server(asyncio.get_running_loop(), ip, port, True)
            logging.info('Successfully connected to server')
            return srv
        except Exception as e:
            logging.error('Cannot connect to server, check settings and try again.')
            logging.exception(e)
            logging.info(f'Retrying in {reconnect_interval} seconds...')
            await asyncio.sleep(reconnect_interval)

def on_stream_update(data):
    """Handle stream update events by switching all groups to the playing stream."""
    if server is None:
        return
    try:
        playing_streams = [s for s in server.streams if s.status == 'playing']
        if not playing_streams:
            return

        selected_stream = playing_streams[0]
        logging.info(f'Active stream detected: {selected_stream.identifier}')

        for group in server.groups:
            asyncio.get_running_loop().create_task(group.set_stream(selected_stream.identifier))

        logging.info(f'Switched all groups to stream: {selected_stream.identifier}')
    except Exception as e:
        logging.error('Error in stream update handler')
        logging.exception(e)

# Main application execution
async def main():
    global server

    while True:
        server = await connect_to_server(serverIp, serverPort)

        try:
            # Register update callbacks for all streams
            for stream in server.streams:
                stream.set_callback(on_stream_update)
                logging.info(f'Registered callback for stream: {stream.identifier}')

            # Keep the application running
            while True:
                await asyncio.sleep(3600)

        except Exception as e:
            logging.error('Unhandled exception in main loop, reconnecting...')
            logging.exception(e)
            await asyncio.sleep(reconnect_interval)

# Entry point with proper asyncio handling
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Stream manager shutting down...")
