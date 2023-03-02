FROM python:3.6.13-slim-bullseye

WORKDIR /app

RUN apt-get -y update && apt-get install -y \
  wget \
  ffmpeg \ 
  libsm6 \
  libxext6

RUN pip install --upgrade setuptools 

COPY requirements.txt .

RUN pip install -r requirements.txt

ADD . . 

CMD gunicorn -k eventlet app:app
