install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer:app run

lint:
	uv run flake8 .

PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	ls -la
	./build.sh

render-start:
	. $HOME/.local/bin/env
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app