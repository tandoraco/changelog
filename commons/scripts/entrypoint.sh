echo "Check for postgres .."

until psql -h "tandora-backend-db-1" -U "postgres" -c '\q'; do
  >&2 echo "Postgres not started - sleeping"
  sleep 5
done


echo "PostgreSQL started"
sleep 2

echo "Install requirements"
pip install -r requirements_dev.txt

echo "Running db migrations"
python manage.py migrate
exec gunicorn tandora.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 600