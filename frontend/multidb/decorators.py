import functools

from django.conf import settings
from dynamic_db_router import in_database

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
                    func(obj, request)

            except Instance.DoesNotExist:
                raise RuntimeError(SUBDOMAIN_DOES_NOT_EXIST_ERROR)

        except KeyError:
            raise RuntimeError(HTTP_HOST_NOT_IN_HEADER_ERROR)

    return wrapper
