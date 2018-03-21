
# parent image
FROM alpine:3.7

# copy python requirements file
COPY requirements.txt /tmp/requirements.txt

# OS installs, pip installs, etc. (https://pkgs.alpinelinux.org/packages)
RUN apk add --no-cache \
    python3=3.6.3-r9 \
    nodejs=8.9.3-r0 \
    nodejs-npm=8.9.3-r0 \
    bash=4.4.19-r1 \
    nginx=1.12.2-r3 \
    uwsgi=2.0.16-r0 \
    uwsgi-python3=2.0.16-r0 \
    supervisor=3.3.3-r1 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install pip setuptools==38.5.1 && \
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

# run node procs
RUN npm install
RUN npm run build

# start server with supervisord
CMD ["/usr/bin/supervisord"]
