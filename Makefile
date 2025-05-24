SHELL=/bin/bash

lint:

	poetry check --lock ; \
	poetry run ruff check src ;

lint-fix:
	poetry run ruff format src ; \
	poetry run ruff check src --fix

test:
	pytest --cov=. --cov-report=term --cov-report=html
