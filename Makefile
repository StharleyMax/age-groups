SHELL := /bin/bash

up:
	docker-compose up -d --build

.PHONY: down
down:
	docker-compose down

localstack-up:
	docker-compose up -d localstack

lint:
	poetry check --lock
	poetry run ruff check src

lint-fix:
	poetry run ruff format src
	poetry run ruff check src --fix

test: localstack-up init-aws-infra
	pytest --cov=src --cov-report=term --cov-report=html

init-aws-infra:
	@echo "Dando permissões ao script..."
	chmod +x infra/localstack/init.sh
	@echo "Executando script de inicialização no LocalStack..."
	docker-compose exec localstack bash -c "chmod +x /etc/localstack/init/ready.d/init.sh && /etc/localstack/init/ready.d/init.sh"


start: up
