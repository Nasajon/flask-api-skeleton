FROM nasajon/nginx:alpine

RUN apk add -U --no-cache \
    ca-certificates \
    python3 \
    postgresql-libs \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    build-base \
    linux-headers \
    pcre-dev

RUN apk add -U --no-cache --virtual .build-deps

COPY conf/requirements.txt /var/www/html/requirements.txt

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r /var/www/html/requirements.txt --no-cache-dir
RUN python3 -m pip install uwsgi
RUN python3 -m pip install --upgrade 'sentry-sdk[flask]==0.13.2'

RUN python3 -m pip install --upgrade boto3

RUN apk --purge del .build-deps

COPY . /var/www/html

COPY conf/nginx.conf /etc/nginx/nginx.conf
COPY conf/entrypoint.sh /
COPY conf/wsgi.ini /etc/wsgi/wsgi.ini

RUN mkdir -p /run/nginx

RUN chmod +x /entrypoint.sh

WORKDIR /var/www/html

ENV PYTHONPATH=/var/www/html

ENV FLASK_APP=/var/www/html/api.py

CMD /entrypoint.sh