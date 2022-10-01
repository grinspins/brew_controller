FROM python:3.10.6-slim-bullseye

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ /etc/timezone

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

RUN pip3 install -e .

EXPOSE 80
