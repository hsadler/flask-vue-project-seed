
# parent image
FROM python:3.9.10-alpine3.15

WORKDIR /server

# OS installs, pip installs, etc. (https://pkgs.alpinelinux.org/packages)
RUN apk add --no-cache \
    bash \
    mariadb-dev \
    build-base 

# python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# the rest is handled by the docker-compose.yaml file
