FROM python:3.6-slim

WORKDIR /finance

COPY requirements.txt .

RUN python -m venv env

RUN env/bin/pip install -r requirements.txt
RUN env/bin/pip install gunicorn pymysql

COPY config.py wsgi.py boot.sh ./
RUN chmod +x boot.sh

COPY migrations migrations
COPY app app

ENV FLASK_APP wsgi.py

EXPOSE 5000

ENTRYPOINT [ "./boot.sh" ]