import os
import asyncio
import snapcast.control
import sys

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

serverIp = os.environ.get('SNAPSERVER_IP')
serverPort = os.environ.get('SNAPSERVER_PORT')

print(f'Snapserver IP: {serverIp}')
print(f'Snapserver Port: {serverPort}')

if serverIp is None:
    print('Snapserver IP not provided, exiting...')
    sys.exit()
if serverPort is None:
    print('Snapserver Port not provided, exiting...')
    sys.exit()

try:
    print('Connecting to server...')
    server = loop.run_until_complete(snapcast.control.create_server(loop, serverIp, serverPort))
except Exception as e:
    print('Cannot connect to server, check settings and try again.')
    print(e)
    sys.exit()

def on_stream_update(data):
    for stream in server.streams:
        if stream.status == 'playing':
            for group in server.groups:
                asyncio.run_coroutine_threadsafe(group.set_stream(stream.identifier), loop)
                print(f'Currently Playing Stream: {stream.identifier}')

try:
    for stream in server.streams:
        stream.set_callback(on_stream_update)

    loop.run_forever()
except Exception as e:
    print('Unhandled exception, check the logs for details.')
    print(e)
    sys.exit()