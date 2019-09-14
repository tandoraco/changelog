import functools

from django.conf import settings
from dynamic_db_router import in_database, DynamicDbRouter

from frontend.multidb.constants import HTTP_HOST_NOT_IN_HEADER_ERROR, SUBDOMAIN_DOES_NOT_EXIST_ERROR
from frontend.multidb.utils import add_instance_to_settings, is_instance_in_settings
from tandoramaster.models import Instance


def change_db(func):

    @functools.wraps(func)
    def wrapper(obj, request):
        if settings.DEBUG:
            return func(obj, request)

        try:
            host = request.META['HTTP_HOST']
            subdomain = host.split(".")[0]

            try:
                instance = Instance.objects.get(subdomain=subdomain)

                if not is_instance_in_settings(instance):
                    add_instance_to_settings(instance)

                with in_database(instance.db_name, write=True):

                    def db_for_read(*args, **kwargs):
                        return instance.db_name

                    def db_for_write(*args, **kwargs):
                        return instance.db_name

                    def default_read_db(*args, **kwargs):
                        return "default"

                    def default_write_db(*args, **kwargs):
                        return "default"

                    DynamicDbRouter.db_for_read = db_for_read
                    DynamicDbRouter.db_for_write = db_for_write

                    func(obj, request)

                    DynamicDbRouter.db_for_read = default_read_db
                    DynamicDbRouter.db_for_write = default_write_db

            except Instance.DoesNotExist:
                raise RuntimeError(SUBDOMAIN_DOES_NOT_EXIST_ERROR)

        except KeyError:
            raise RuntimeError(HTTP_HOST_NOT_IN_HEADER_ERROR)

    return wrapper
