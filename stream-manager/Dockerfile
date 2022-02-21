FROM python:slim-bullseye
LABEL Author Rogger Fabri

RUN apt update && apt upgrade -y \ 
 && python -m pip install --upgrade pip \
 && pip install snapcast \
 && rm -rf /var/lib/apt/lists/*

COPY stream_manager.py stream_manager.py

CMD [ "python","-u","./stream_manager.py" ]
