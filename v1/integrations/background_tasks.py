from background_task import background
from django.apps import apps

from v1.integrations.twitter.handlers import TwitterBackgroundJobHandler
from v1.integrations.webhooks.handlers import WebhookBackgroundJobHandler
from v1.integrations.zapier.handlers import ZapierBackgroundJobHandler

# key should be model name
INTEGRATION_BACKGROUND_JOB_HANDLER_MAP = {
    'Zapier': ZapierBackgroundJobHandler,
    'Webhooks': WebhookBackgroundJobHandler,
    'Twitter': TwitterBackgroundJobHandler,
}


@background(schedule=1)
def trigger_integration_background_tasks(company_id, changelog_id, **kwargs):
    company_model = apps.get_model('v1', 'Company')
    changelog_model = apps.get_model('v1', 'Changelog')
    try:
        company = company_model.objects.get(id=company_id)
        changelog = changelog_model.objects.get(id=changelog_id)
    except (company_model.DoesNotExist, changelog_model.DoesNotExist):
        pass  # todo log
    else:
        for integration_name, background_job_handler in INTEGRATION_BACKGROUND_JOB_HANDLER_MAP.items():
            integration_model_class = apps.get_model('v1', integration_name)
            try:
                integration_obj = integration_model_class.objects.get(company=company, active=True)
            except integration_model_class.DoesNotExist:
                pass  # todo log
            else:
                handler = background_job_handler(company, integration_obj, changelog)
                handler.execute(**kwargs)
