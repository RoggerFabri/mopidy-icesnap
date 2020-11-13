FROM python:slim

ARG SNAPSERVER

RUN pip install snapcast
COPY stream_manager.py stream_manager.py

CMD [ "python","-u","./stream_manager.py" ]