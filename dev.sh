
docker build \
	-f Dockerfile.dev \
	-t flask-server:dev . && \
docker run \
	--name 'dev-server' \
	--rm \
	-v `pwd`/app:/app \
	-p 4000:80 \
	flask-server:dev \
	/usr/bin/supervisord
