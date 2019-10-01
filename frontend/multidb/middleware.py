from django.utils.deprecation import MiddlewareMixin

from frontend.multidb.decorators import change_db


class DBSwitchMiddleware(MiddlewareMixin):

    @change_db
    def process_request(self, request):
        pass
