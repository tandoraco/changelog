#!/usr/bin/env bash
echo "Install requirements"
pip install -r requirements_dev.txt

echo "Running db migrations"
python manage.py migrate

pip install newrelic
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program
newrelic-admin run-program
exec gunicorn tandora.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --timeout 600