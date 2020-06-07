import os
import asyncio
import snapcast.control
import sys
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
server = loop.run_until_complete(snapcast.control.create_server(loop, 'SNAPSERVER', 1705))

def on_stream_update(data):
    for stream in server.streams:
        if stream.status == 'playing':
            for group in server.groups:
                asyncio.run_coroutine_threadsafe(group.set_stream(stream.identifier), loop)

try:
    for stream in server.streams:
        stream.set_callback(on_stream_update)

    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.close()