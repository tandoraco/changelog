from django.db import models


class AuditLog(models.Model):
    company = models.ForeignKey('Company', on_delete=models.DO_NOTHING)
    resource_name = models.CharField(max_length=20)
    resource_id = models.PositiveIntegerField()
    action = models.CharField(max_length=10)
    performed_by = models.CharField(max_length=50)
    source = models.CharField(max_length=10)
    endpoint = models.CharField(max_length=50)
    payload = models.TextField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=250, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.action} {self.resource_name} by {self.performed_by}'
