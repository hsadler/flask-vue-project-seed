
# parent image
FROM node:17.4.0-alpine3.15

WORKDIR /client

ENV NODE_OPTIONS=--openssl-legacy-provider

# OS installs, pip installs, etc. (https://pkgs.alpinelinux.org/packages)
RUN apk add --no-cache \
    npm \
    bash

COPY ./package.json package.json
RUN npm i

# the rest is handled by the docker-compose.yaml file
