from django.core.management import BaseCommand
from django.db import transaction

from v1.accounts.models import Company, User
from v1.categories.models import Category
from v1.core.models import Changelog


class Command(BaseCommand):
    description = "Permanently delete a company from database."

    def add_arguments(self, parser):
        parser.add_argument('company_name', type=str, help='Company to be deleted.')

    @transaction.atomic
    def handle(self, *args, **options):
        company_name = options.get('company_name')
        company_name = str(company_name).lower()

        try:
            company = Company.objects.get(company_name__iexact=company_name)
            Changelog.objects.filter(company=company).delete()
            Category.objects.filter(company=company).delete()
            users = User.objects.filter(company=company)
            users.update(company=None)
            users.delete()
            company.delete()
        except Company.DoesNotExist:
            print('Company does not exist')
