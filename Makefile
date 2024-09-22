BACKEND_SERVICE ?= web
ALEMBIC_INI_PATH ?= ./alembic.ini

include .env

.PHONY:  build up down lint inside-container help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile \
	| awk 'BEGIN{FS=":.*## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Build the docker image
	docker-compose build

up: build ## Up the docker-compose
	docker-compose up

down: ## Down the docker-compose
	docker-compose down --remove-orphans

revision: build
	docker compose run ${BACKEND_SERVICE} alembic -c ${ALEMBIC_INI_PATH} revision --autogenerate -m "$(m)"

upgrade-version:
	docker compose run ${BACKEND_SERVICE} alembic -c ${ALEMBIC_INI_PATH} upgrade head

downgrade-version:
	docker compose run ${BACKEND_SERVICE} alembic -c ${ALEMBIC_INI_PATH} downgrade ${n}

install: ## Install all dependencies
	pip install -r requirements.txt

lint: ## Run linters
	pre-commit run --all-files

inside-container: ## Enter inside the container
	docker compose exec ${BACKEND_SERVICE} sh
