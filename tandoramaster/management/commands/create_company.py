import json
import pathlib
from datetime import datetime

import pytz
from django.core.management import BaseCommand
from django.db import transaction

from v1.accounts.constants import CHANGELOG_TERMINOLOGY
from v1.accounts.models import Referral
from v1.accounts.serializers import CompanySerializer
from v1.categories.models import Category
from v1.core.models import Changelog


def get_current_utc_time():
    current_time = datetime.utcnow()
    return str(current_time.replace(tzinfo=pytz.utc))


class Command(BaseCommand):
    description = "Create a company and populate initial data."

    def add_arguments(self, parser):
        parser.add_argument('-e', '--email', type=str, help='Email address of company admin')
        parser.add_argument('-n', '--name', type=str, help='Admin name')
        parser.add_argument('-p', '--password', type=str, help='Password')
        parser.add_argument('-c', '--company_name', type=str, help='Company name')
        parser.add_argument('-w', '--website', type=str, help='Company website address')
        parser.add_argument('-ct', '--changelog_terminology', type=str, help='How the company wants to name changelog?')
        parser.add_argument('-ref', '--referral_code', type=str, help='Code to track conversion from affiliates.')

    @transaction.atomic
    def handle(self, *args, **options):
        email = options.get('email')
        name = options.get('name')
        password = options.get('password')
        company_name = options.get('company_name')
        website = options.get('website')
        terminology = options.get('changelog_terminology', CHANGELOG_TERMINOLOGY)
        referral_code = options.get('referral_code')

        if not (email and name and password and company_name and website and terminology):
            raise AssertionError("All required arguments are not present.")

        self.stdout.write(f"Creating company ..")

        data = {
            'company_name': company_name,
            'website': website,
            'changelog_terminology': terminology,
            'email': email,
            'name': name,
            'password': password
        }

        company_serializer = CompanySerializer(data=data)
        company = None
        if company_serializer.is_valid():
            company = company_serializer.save()
        else:
            self.stderr.write("Creating company failed", style_func=self.style.ERROR)
            print(company_serializer.errors)
            raise RuntimeError('Creating company failed')

        self.stdout.write(f"Populating initial data ..")

        current_path = pathlib.Path(__file__).parent
        initial_data_json = current_path / 'initial_data.json'

        with open(initial_data_json) as initial_data:
            data = json.loads(initial_data.read())

            categories = list()
            for category in data['categories']:
                category['company'] = company
                categories.append(Category(**category))

            Category.objects.bulk_create(categories)

            new_category = Category.objects.get(company=company, name='New')

            changelog = data['changelog']
            changelog['company'] = company
            changelog['category'] = new_category
            changelog['created_by'] = company.admin
            changelog['last_edited_by'] = company.admin
            created_changelog = Changelog.objects.create(**changelog)

        if referral_code:
            try:
                referral = Referral.objects.get(referral_code=referral_code)
                referral.add_signup(company.id)
            except Referral.DoesNotExist:
                pass

        success_data = {
            'company_id': company.id,
            'created_changelog_id': created_changelog.id,
            'new_category_id': new_category.id
        }

        self.stdout.write(f"Done creating company .. {success_data}", style_func=self.style.SUCCESS)
