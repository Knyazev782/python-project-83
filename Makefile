install:
	uv sync

dev:
	.venv/bin/flask --debug --app page_analyzer:app run

lint:
	.venv/bin/flake8 .

PORT ?= 8000
start:
	.venv/bin/gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	ls -la
	./build.sh

render-start:
	.venv/bin/gunicorn -w 5 -b 0.0.0.0:8001 page_analyzer:app