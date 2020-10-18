FROM python:3.7.2-alpine

RUN apk add --update --no-cache python3-dev gcc musl-dev libffi-dev openssl-dev postgresql-dev musl-dev postgresql vim
RUN apk add py-cryptography

COPY . /code/
WORKDIR /code

RUN apk add build-base py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib

RUN pip install --upgrade pip
RUN pip install -r requirements_dev.txt --use-feature=2020-resolver
RUN pip install django-storages==1.8
ENV PYTHONUNBUFFERED=1
