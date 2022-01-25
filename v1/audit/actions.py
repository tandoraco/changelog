import json

from sentry_sdk.integrations.wsgi import get_client_ip

from v1.audit.models import AuditLog, LoginAuditLog

ACTION_MAP = {
    'get': 'read',
    'post': 'create',
    'patch': 'update',
    'delete': 'destroy',
    'put': 'update'
}


class AuditLogAction:

    def __init__(self, request, resource, source):
        self.request = request
        self.resource = resource
        self.source = source

    def set_audit_log(self, action=None, **kwargs):
        if self.request.method.lower() in {'post', 'patch'}:
            if hasattr(self.request, 'data'):
                request_data = json.dumps(self.request.data)
            elif hasattr(self.request, 'POST'):
                post_data = self.request.POST.copy()
                post_data.pop('csrfmiddlewaretoken', None)
                request_data = json.dumps(post_data)
            else:
                request_data = None
        else:
            request_data = None
        data = {
            'company': self.request.user.company,
            'resource_name': self.resource.__class__.__name__,
            'resource_id': self.resource.id,
            'action': action or ACTION_MAP.get(self.request.method.lower()),
            'performed_by': str(self.request.user.email),
            'source': self.source,
            'endpoint': self.request.path,
            'payload': request_data,
            'ip_address': get_client_ip(self.request.META),
            'user_agent': self.request.META.get('HTTP_USER_AGENT')
        }
        AuditLog.objects.create(**data)


class LoginAuditLogAction(AuditLogAction):

    def set_audit_log(self, action=None, **kwargs):
        data = {
            'source': self.source,
            'ip_address': get_client_ip(self.request.META),
            'user_agent': self.request.META.get('HTTP_USER_AGENT'),
        }
        data.update(kwargs)
        data.pop('action', None)
        LoginAuditLog.objects.create(**data)
