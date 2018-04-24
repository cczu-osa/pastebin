FROM python:3.6
MAINTAINER Weicheng Jiang "williamjiang97@gmail.com"
ADD . /flask_compose
WORKDIR /flask_compose
RUN pip install -r requirements.txt