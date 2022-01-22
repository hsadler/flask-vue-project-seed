
# dev

up-dev:
	docker-compose -f docker-compose.dev.yml up --build --force-recreate \
	--remove-orphans --abort-on-container-exit

app-shell-dev:
	docker exec -it flask-vue-dev /bin/sh

mysql-shell-dev:
	docker exec -it flask-vue-mysql-dev mysql -uroot -ppassword

redis-shell-dev:
	docker exec -it flask-vue-redis-dev /bin/sh


# prod

up-prod:
	docker-compose -f docker-compose.yml up --build --force-recreate \
	--remove-orphans --abort-on-container-exit

app-shell-prod:
	docker exec -it flask-vue /bin/sh

mysql-shell-prod:
	docker exec -it flask-vue-mysql mysql -uroot -ppassword

redis-shell-prod:
	docker exec -it flask-vue-redis /bin/sh
	