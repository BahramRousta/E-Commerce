FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY . /code/

EXPOSE 8000

RUN pip install --upgrade pip

COPY requirements.txt /code/

RUN pip install -r requirements.txt
