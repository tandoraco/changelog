from django.db import connections

from tandora import settings


def add_instance_to_settings(instance):
    db = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': instance.db_name,
        'USER': instance.db_user,
        'HOST': instance.db_host,
        'PORT': instance.db_port
    }

    if instance.db_password:
        db['PASSWORD'] = instance.db_password

    if instance.db_name not in settings.DATABASES:
        settings.DATABASES[instance.db_name] = db
        connections.databases[instance.db_name] = db
        print(settings.DATABASES)


def is_instance_in_settings(instance):
    return instance.db_name in settings.DATABASES
