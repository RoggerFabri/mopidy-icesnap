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

logging.info(f'SNAPSERVER_IP: {serverIp}')
logging.info(f'SNAPSERVER_PORT: {serverPort}')

# Validate required configuration
if serverIp is None:
    logging.error('ENV|SNAPSERVER_IP not provided, exiting...')
    sys.exit(1)
if serverPort is None:
    logging.error('ENV|SNAPSERVER_PORT not provided, exiting...')
    sys.exit(1)

async def connect_to_server(ip: str, port: str) -> Optional[snapcast.control.server]:
    """Establish connection to the Snapcast server."""
    try:
        logging.info(f'Connecting to server at {ip}:{port}...')
        server = await snapcast.control.create_server(asyncio.get_event_loop(), ip, port, True)
        logging.info('Successfully connected to server')
        return server
    except Exception as e:
        logging.error('Cannot connect to server, check settings and try again.')
        logging.exception(e)
        return None

def on_stream_update(data):
    """Handle stream update events by switching all groups to the playing stream."""
    for server_stream in server.streams:
        if server_stream.status == 'playing':
            for group in server.groups:
                loop.create_task(group.set_stream(server_stream.identifier))
            logging.info(f'Switched all groups to stream: {server_stream.identifier}')
            break  # Only use the first playing stream

# Main application execution
async def main():
    global server
    
    server = await connect_to_server(serverIp, serverPort)
    if not server:
        sys.exit(1)
        
    try:
        # Register update callbacks for all streams
        for stream in server.streams:
            stream.set_callback(on_stream_update)
            logging.info(f'Registered callback for stream: {stream.identifier}')
        
        # Keep the application running
        while True:
            await asyncio.sleep(3600)  # Just to keep the main task alive
            
    except Exception as e:
        logging.error('Unhandled exception in main loop.')
        logging.exception(e)
        sys.exit(1)

# Entry point with proper asyncio handling
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logging.info("Stream manager shutting down...")
    finally:
        loop.close()