FROM python:3.7.2-alpine

RUN apk add --update --no-cache python3-dev gcc musl-dev libffi-dev openssl-dev postgresql-dev musl-dev postgresql
RUN pip install cryptography==2.2.2

COPY . /code/
WORKDIR /code
RUN pip install -r requirements_dev.txt
ENV PYTHONUNBUFFERED=1

RUN apk add build-base py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib
RUN pip install pillow==6.0.0
