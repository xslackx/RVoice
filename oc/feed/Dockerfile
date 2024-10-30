FROM alpine:3.18

RUN apk update && \
apk add python3 \
py3-pip && \
adduser feed -D && \
su -l feed && \
cd /home/feed && \
mkdir app && \
cd app && \
wget https://github.com/xslackx/RVoice/archive/refs/heads/master.zip -O rvoice.zip && \
unzip rvoice.zip && \
mv RVoice-master rvoice && \
cd rvoice && \
python3 -m venv . && \
source bin/activate && \
pip install -r requirements.txt

ENTRYPOINT su -l feed -c "source /home/feed/app/rvoice/bin/activate && python3 /home/feed/app/rvoice/client.py"