#!/bin/sh

python3 manage.py migrate
python3 manage.py collectstatic --noinput

python3 manage.py runserver 0.0.0.0:8000
# gunicorn -w $(nproc) --bind 0.0.0.0:8000 wsgi
