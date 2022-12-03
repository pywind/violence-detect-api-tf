FROM python:3.8-slim
ARG port

USER root


COPY . /app

WORKDIR /app

ADD start.sh /

RUN chmod +x /start.sh

#ENV PORT=$port

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
    && apt-get -y install curl \
    && apt-get install libgomp1 \
    && apt-get install libgl1 ffmpeg libsm6 libxext6  -y


RUN chgrp -R 0 /app \
    && chmod -R g=u /app \
    && pip install pip --upgrade \
    && pip install -r requirements.txt
EXPOSE 3000

CMD ["/start.sh"]
