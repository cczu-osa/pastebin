FROM python:alpine
MAINTAINER Weicheng Jiang "williamjiang97@gmail.com"
ADD . /pastebin
WORKDIR /pastebin
RUN pip install --no-cache-dir -r requirements.txt
CMD ./run.sh
