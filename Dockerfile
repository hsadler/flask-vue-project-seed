
# parent image
FROM alpine:3.6

# copy python requirements file
COPY requirements.txt /tmp/requirements.txt

# OS installs, pip installs, etc. (https://pkgs.alpinelinux.org/packages)
RUN apk add --no-cache \
    python3 \
    python3-dev \
    nodejs \
    nodejs-npm \
    bash \
    mariadb-dev \
    build-base \
    supervisor \
    nginx \
    uwsgi \
    uwsgi-python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install pip setuptools && \
    pip3 install -r /tmp/requirements.txt && \
    rm /etc/nginx/conf.d/default.conf && \
    rm -r /root/.cache

# copy the Nginx global conf
COPY config/nginx.conf /etc/nginx/

# copy the Flask Nginx site conf
COPY config/flask-app-nginx.conf /etc/nginx/conf.d/

# copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY config/uwsgi.ini /etc/uwsgi/

# copy custom Supervisord config
COPY config/supervisord.conf /etc/supervisord.conf

# copy app
COPY ./app /app
WORKDIR /app

# npm installs
COPY app/client/package.json /tmp/package.json
RUN cd /tmp && \
    npm install && \
    mkdir -p /app/client && \
    cp -a /tmp/node_modules /app/client/

# npm build
RUN cd /app/client && \
    npm run build

# the rest is handled by the docker-compose.yml file
