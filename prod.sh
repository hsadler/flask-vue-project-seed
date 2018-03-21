
docker build \
	-t flask-server . && \
docker run \
	--name 'prod-server' \
	--rm \
	-p 80:80 flask-server
