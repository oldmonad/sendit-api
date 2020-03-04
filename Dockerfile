FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

RUN pip install --no-cache-dir -r /requirements.txt

RUN apk del .tmp-build-deps

RUN mkdir /sendit
WORKDIR /sendit
COPY ./sendit /sendit
