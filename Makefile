migrate: migrations
	python3 manage.py migrate

migrations:
	python3 manage.py makemigrations

run:
	python3 manage.py runserver

dump:

populate:csu

csu:
	python3 manage.py csu

test:
	python3 manage.py test
