FROM python:3.7-buster

RUN mkdir app
WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH="/services/backend"

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src/ .