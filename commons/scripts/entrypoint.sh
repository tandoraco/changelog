sh wait-for-db.sh

echo "Running db migrations"
python manage.py migrate
exec gunicorn tandora.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 600