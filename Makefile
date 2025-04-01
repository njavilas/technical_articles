include .env

VENV=/home/vscode/venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

install:
	$(PIP) install -r requirements.txt
	$(PIP) install --upgrade pip

lint:
	export PYTHONPATH=$(PWD)
	$(VENV)/bin/black .
	$(VENV)/bin/pylint .
	
clean:
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -delete
	find . -name '*.pyi' -delete

init:
	etcdctl --endpoints=http://localhost:2379 put "config/database_url" "sqlite://db.sqlite3"
	etcdctl --endpoints=http://localhost:2379 put "config/server_http_port" "8000"

	etcdctl --endpoints=http://localhost:2379 get "config/server_http_port"
	etcdctl --endpoints=http://localhost:2379 get "config/database_url"

drop: clean
	rm db.sqlite3

push:
	git add .
	git commit -m "auto update"
	git push origin main

build:
	docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .

ci:
	gitlab-ci-local --privileged build

run:
	uvicorn main:app --reload