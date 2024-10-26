FROM alpine:3.18
MAINTAINER https://github.com/xslackx

RUN apk update && \
apk add python3 \
py3-pip && \
adduser feed -D && \
su -l feed && \
cd /home/feed && \
mkdir app && \
cd app && \
wget https://github.com/xslackx/feedrss/archive/refs/heads/master.zip -O feedrss.zip && \
unzip feedrss.zip && \
mv feedrss-master feedrss && \
cd feedrss && \
python3 -m venv . && \
source bin/activate && \
pip install -r requirements.txt