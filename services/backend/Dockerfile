FROM debian:buster-slim

RUN mkdir app
WORKDIR /app

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install python3 \
    python3-pip \
    python3-opencv

# See https://github.com/waveform80/picamera/issues/578
ENV READTHEDOCS=True

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH="/services/backend"

COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY src/ .
