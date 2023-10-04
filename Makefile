dev-pg:
	docker run --name randevu-pg-local -p 45045:5432 -e POSTGRES_USER=rnadmin \
		-e POSTGRES_PASSWORD=secret -e POSTGRES_DB=randevu.local -d postgres

dev-redis:
	docker compose --env-file .env -f docker-compose.prod.yml run -d --service-ports redis

build:
	docker compose -f docker-compose.build.yml build

install-dev-deps: dev-deps
	pip-sync requirements.txt dev-requirements.txt

install-deps: deps
	pip-sync requirements.txt

deps:
	pip install --upgrade pip pip-tools
	pip-compile requirements.in

dev-deps: deps
	pip-compile dev-requirements.in

server:
	cd cd src && ./manage.py migrate && ./manage.py runserver 54340

worker:
	cd src && celery -A app worker -E --purge

lint:
	cd src && ./manage.py makemigrations --check --no-input --dry-run
	flake8 cd src
	cd src && mypy

test:
	cd src && pytest -n 4 --ff -x --create-db --cov-report=xml --cov=. -m 'not single_thread'