NAME=askoldova
include variables.mk
export VERSION MYSQL_DATABASE MYSQL_USER MYSQL_PASSWORD MYSQL_ROOT_PASSWORD

up:
	docker-compose -p $(NAME) up -d

pull:
	docker-compose pull

build:
	docker-compose -p $(NAME) build

stop:
	docker-compose -p $(NAME) stop

ps:
	docker-compose -p $(NAME) ps

rm_mysql:
	docker-compose -p $(NAME) rm mysql

exec_mysql:
	docker exec -it -u apps $(NAME)_mysql_1  bash

rm: rm_mysql
