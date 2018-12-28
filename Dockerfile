FROM python:3.7-rc-alpine
MAINTAINER Weicheng Jiang "williamjiang97@gmail.com"
ADD . /flask_compose
WORKDIR /flask_compose
RUN apk update && apk add tzdata \
&& ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& echo "Asia/Shanghai" > /etc/timezone \
&& pip install --no-cache-dir -r requirements.txt
CMD gunicorn -w 4 -b 0.0.0.0:80 PasteBinWeb:app
