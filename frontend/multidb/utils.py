from tandora import settings


def add_instance_to_settings(instance, db_key):
    db = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': instance.db_name,
        'USER': instance.db_user,
        'HOST': instance.db_host,
        'PORT': instance.db_port
    }

    if instance.db_password:
        db['PASSWORD'] = instance.db_password

    if db_key not in settings.DATABASES:
        settings.DATABASES[db_key] = db


def check_instance_in_settings(db_key):
    return db_key in settings.DATABASES
