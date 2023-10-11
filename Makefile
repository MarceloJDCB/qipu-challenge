DOCKER_COMPOSE_FILE=$(shell echo -f docker-compose.yml)

_rebuild:
	docker-compose ${DOCKER_COMPOSE_FILE} down
	docker-compose ${DOCKER_COMPOSE_FILE} build --no-cache --force-rm

rebuild:
	docker-compose ${DOCKER_COMPOSE_FILE} down
	docker-compose ${DOCKER_COMPOSE_FILE} build

up:
	docker-compose ${DOCKER_COMPOSE_FILE} up -d --remove-orphans

aisweb:
	docker-compose exec qipu python 2_Aisweb/ais_data_scrap.py

build: stopall
	docker-compose ${DOCKER_COMPOSE_FILE} up -d --remove-orphans --build

lista_encadeada:
	docker-compose exec qipu python 1_ListaEncadeada/lista_encadeada.py

logs:
	docker-compose ${DOCKER_COMPOSE_FILE} logs --tail 200

down:
	docker-compose ${DOCKER_COMPOSE_FILE} down --remove-orphans

stopall:
	docker-compose ${DOCKER_COMPOSE_FILE} stop
