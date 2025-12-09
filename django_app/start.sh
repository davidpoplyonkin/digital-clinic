#!/bin/sh
python manage.py migrate --noinput
exec python -m gunicorn --bind 0.0.0.0:8000 digital_clinic.wsgi