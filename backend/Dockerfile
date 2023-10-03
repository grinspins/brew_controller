FROM python:3.11-slim-bullseye

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ /etc/timezone

RUN mkdir /app
WORKDIR /app

RUN pip3 install poetry==1.6.1

COPY pyproject.toml poetry.lock .
RUN poetry install

COPY . .

RUN pip3 install -e .

EXPOSE 80
