SHELL:=/bin/bash

DOCKER_IMAGE=categories_api:latest

build:
	docker build \
		--file Dockerfile \
		--tag $(DOCKER_IMAGE) \
	.

test:
	src/manage.py test
