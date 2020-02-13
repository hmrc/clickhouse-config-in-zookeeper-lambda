SHELL := /bin/bash
PWD = $(shell pwd)

IMAGE_NAME := hmrc/clickhouse_config_in_zookeeper

default: help

help: ## The help text you're reading
	@grep --no-filename -E '^[a-zA-Z1-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Build all the Python Docker images
	@docker build -f docker/Dockerfile-3.6 -t $(IMAGE_NAME)-3.6 .
	@docker build -f docker/Dockerfile-3.7 -t $(IMAGE_NAME)-3.7 .
	@docker build -f docker/Dockerfile-3.8 -t $(IMAGE_NAME)-3.8 .
.PHONY: build

sh-37: ## Get a terminal in a Python 3.7 container
	@docker run --rm -it $(IMAGE_NAME)-3.7 bash
.PHONY: sh-37

test: ## Run unit tests
	@docker run --rm -v $(PWD)/app $(IMAGE_NAME)-3.6 nosetests -v --with-cover --cover-erase --cover-package=clickhouse_config_in_zookeeper tests/*.py
	@docker run --rm -v $(PWD)/app $(IMAGE_NAME)-3.7 nosetests -v --with-cover --cover-erase --cover-package=clickhouse_config_in_zookeeper tests/*.py
	@docker run --rm -v $(PWD)/app $(IMAGE_NAME)-3.8 nosetests -v --with-cover --cover-erase --cover-package=clickhouse_config_in_zookeeper tests/*.py
.PHONY: test
