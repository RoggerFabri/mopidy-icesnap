FROM python:slim
LABEL Author Rogger Fabri

RUN pip install snapcast
COPY stream_manager.py stream_manager.py

CMD [ "python","-u","./stream_manager.py" ]