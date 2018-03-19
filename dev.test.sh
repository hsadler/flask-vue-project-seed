
docker build -f Dockerfile.dev -t flask-server:dev . && \
docker run -it flask-server:dev sh
