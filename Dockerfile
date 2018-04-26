FROM python:3.6
MAINTAINER Weicheng Jiang "williamjiang97@gmail.com"
ADD . /flask_compose
WORKDIR /flask_compose
RUN pip install --no-cache-dir -r requirements.txt
CMD gunicorn -w 4 -b 8.8.8.8:80 PasteBinWeb:app