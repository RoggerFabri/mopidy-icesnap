import os
import asyncio
import snapcast.control
import sys
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%d-%m-%Y %H:%M:%S')

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
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(snapcast.control.create_server(loop, serverIp, serverPort))
except Exception as e:
    logging.error('Cannot connect to server, check settings and try again.')
    logging.exception(e)
    sys.exit()

def on_stream_update():
    for stream in server.streams:
        if stream.status == 'playing':
            for group in server.groups:
                loop.create_task(group.set_stream(stream.identifier))

try:
    for stream in server.streams:
        stream.set_callback(on_stream_update)

    loop.run_forever()
except Exception as e:
    logging.error('Unhandled exception, check the logs for details.')
    logging.exception(e)
    sys.exit()