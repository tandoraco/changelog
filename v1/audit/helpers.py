from django.utils.text import slugify
from sentry_sdk.integrations.wsgi import get_client_ip

from v1.audit.models import PublicPageView, PublicPageViewAudit


def audit_public_page_request(request, company_name, slug=''):
    path = f'/{slugify(company_name)}/{slug}'
    page_view, _ = PublicPageView.objects.get_or_create(path=path)
    page_view.count += 1
    page_view.save()

    PublicPageViewAudit.objects.create(public_page_view=page_view, ip_address=get_client_ip(request.META),
                                       user_agent=request.META.get('HTTP_USER_AGENT'))
