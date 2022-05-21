import os
import asyncio
import snapcast.control
import sys
import time
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%d-%m-%Y %H:%M:%S')

loop = asyncio.get_event_loop()

serverIp = os.environ.get('SNAPSERVER_IP')
serverPort = os.environ.get('SNAPSERVER_PORT')

logging.info(f'SNAPSERVER_IP: {serverIp}')
logging.info(f'SNAPSERVER_PORT: {serverPort}')

if serverIp is None:
    logging.error('ENV|SNAPSERVER_IP not provided, exiting...')
    sys.exit()
if serverPort is None:
    logging.error('ENV|SNAPSERVER_PORT not provided, exiting...')
    sys.exit()

try:
    logging.info('Connecting to server...')
    server = loop.run_until_complete(snapcast.control.create_server(loop, serverIp, serverPort))
except Exception as e:
    logging.error('Cannot connect to server, check settings and try again.')
    logging.exception(e)
    sys.exit()

def get_playing_stream():
    for stream in server.streams:
        if stream.status == 'playing':
            return stream.identifier

def update_stream_in_groups(stream):
    logging.info('Updating playing stream to: %s', stream)
    for group in server.groups:
        group.set_stream(stream)

try:
    stream = ""
    while True:
        time.sleep(1)
        playing_stream = get_playing_stream()
        if stream != playing_stream:
            stream = playing_stream
            logging.info('Currently playing stream: %s', stream)
            update_stream_in_groups(stream)
            
except Exception as e:
    logging.error('Unhandled exception, check the logs for details.')
    logging.exception(e)
    sys.exit()