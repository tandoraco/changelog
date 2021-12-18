run-tests:
	pip install -r requirements_dev.txt;
	pytest --test-group-count 4 --test-group=$(STEP_NO) -n 4

dev-up:
	docker compose -f dev.yml up -d
	docker attach $(shell basename $(CURDIR))-web-1

dev-bash:
	docker exec -it  $(shell basename $(CURDIR))-web-1 /bin/sh

run-migration:
	python manage.py makemigrations
	python manage.py migrate
