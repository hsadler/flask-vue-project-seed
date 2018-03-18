
docker build -f Dockerfile.dev -t flask-server:dev . && \
docker run -p 4000:80 flask-server:dev
