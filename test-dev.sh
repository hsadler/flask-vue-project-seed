
docker build \
	-f Dockerfile.dev \
	-t flask-server:dev . && \
docker run \
	--name 'dev-server' \
	-it \
	--rm \
	-v `pwd`/app:/app \
	-p 4000:80 \
	flask-server:dev \
	/bin/bash
