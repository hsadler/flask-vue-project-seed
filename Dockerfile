
# parent image
FROM alpine:3.7

# Copy python requirements file
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

# Copy the Nginx global conf
COPY nginx.conf /etc/nginx/

# Copy the Flask Nginx site conf
COPY flask-app-nginx.conf /etc/nginx/conf.d/

# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY uwsgi.ini /etc/uwsgi/

# Custom Supervisord config
COPY supervisord.conf /etc/supervisord.conf

# Add demo app
COPY ./app /app
WORKDIR /app

RUN npm install
RUN npm run build

CMD ["/usr/bin/supervisord"]
