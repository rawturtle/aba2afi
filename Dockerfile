# Docker Development Enviroment

FROM python:2.7
MAINTAINER RR
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
#ADD requirements.txt /code/
#RUN pip install -r requirements.txt
ADD . /code/