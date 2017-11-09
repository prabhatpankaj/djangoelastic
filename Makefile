.PHONY: install lmigrate clear prun lrun

install:
	pip install --upgrade setuptools pip
	pip install -r requirements.txt

migrate:
	python djangoelastic/manage.py makemigrations
	python djangoelastic/manage.py migrate

run:
	python djangoelastic/manage.py runserver 0.0.0.0:8080
