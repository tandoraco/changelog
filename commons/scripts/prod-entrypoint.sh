#!/usr/bin/env bash
echo "Install requirements"
pip install -r requirements_dev.txt

echo "Running db migrations"
python manage.py migrate

exec gunicorn tandora.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 6 \
    --timeout 600