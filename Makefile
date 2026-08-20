.PHONY: install migrate collectstatic dev render-start build lint test test-coverage

install:
	uv sync

migrate:
	.venv/bin/python manage.py migrate

collectstatic:
	.venv/bin/python manage.py collectstatic --noinput

dev:
	uv run python manage.py runserver

render-start:
	PATH="$(CURDIR)/.venv/bin:$$PATH" gunicorn task_manager.wsgi

build:
	./build.sh

lint:
	uv run ruff check .

test:
	uv run pytest

test-coverage:
	uv run pytest --cov=. --cov-report=xml:coverage.xml --cov-report=term