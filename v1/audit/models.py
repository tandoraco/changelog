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


class PublicPageView(models.Model):
    path = models.CharField(max_length=500, unique=True)
    count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.path} - {self.count}'


class PublicPageViewAudit(models.Model):
    public_page_view = models.ForeignKey('PublicPageView', on_delete=models.DO_NOTHING)
    user_agent = models.CharField(max_length=250, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.public_page_view} - {self.user_agent} - {self.ip_address}'
