import requests
from django.conf import settings
from django.core.management import BaseCommand
from django.utils.text import slugify

from v1.accounts.models import Company


class Command(BaseCommand):
    def handle(self, *args, **options):

        for company in Company.objects.all():
            print(company)
            if not company.admin:
                print('Skipping. Admin not present.')
                continue

            company_name = slugify(company.company_name)
            company.website = f'https://byol.ink/{company_name}'
            company.save()

            data = {
                'user_name': company_name,
                'company_name': company_name
            }

            url = "https://byol.ink/tc/biolink"
            headers = {
                'Authorization': f'Bearer {settings.TANDORA_CHANGELOG_KEY}'
            }

            resp = requests.post(url, data=data, headers=headers)

            if resp:
                print('success')
            else:
                print(resp.content)
