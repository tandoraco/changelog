import json

from sentry_sdk.integrations.wsgi import get_client_ip

from v1.audit.models import AuditLog

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

    def set_audit_log(self):
        data = {
            'company': self.request.user.company,
            'resource_name': self.resource.__class__.__name__,
            'resource_id': self.resource.id,
            'action': ACTION_MAP.get(self.request.method.lower()),
            'performed_by': str(self.request.user.email),
            'source': self.source,
            'endpoint': self.request.path,
            'payload': json.dumps(self.request.data) if self.request.method.lower() in {'post', 'patch'} else None,
            'ip_address': get_client_ip(self.request.META),
            'user_agent': self.request.META.get('HTTP_USER_AGENT')
        }
        AuditLog.objects.create(**data)
