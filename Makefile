
up:
	docker-compose -f docker-compose.dev.yml up --build --force-recreate \
	--remove-orphans --abort-on-container-exit

app-shell:
	docker exec -it flask-vue-dev /bin/sh

mysql-shell:
	docker exec -it flask-vue-mysql-dev mysql -uroot -ppassword

redis-shell:
	docker exec -it flask-vue-redis-dev /bin/sh
	