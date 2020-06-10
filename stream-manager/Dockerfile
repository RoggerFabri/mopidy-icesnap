FROM python:slim

ARG SNAPSERVER

RUN pip install snapcast
COPY stream_manager.py stream_manager.py

RUN sed -i "s/SNAPSERVER/${SNAPSERVER}/g" stream_manager.py

CMD [ "python","-u","./stream_manager.py" ]