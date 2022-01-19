FROM python:3.11.0a3-slim-bullseye
LABEL Author Rogger Fabri

RUN pip install snapcast
COPY stream_manager.py stream_manager.py

CMD [ "python","-u","./stream_manager.py" ]