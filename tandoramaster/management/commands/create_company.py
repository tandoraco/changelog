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


def create_changelog(changelog, category, company):
    changelog['company'] = company
    changelog['category'] = category
    changelog['created_by'] = company.admin
    changelog['last_edited_by'] = company.admin
    return Changelog.objects.create(**changelog)


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
        parser.add_argument('-uc', '--use_case', type=str, help='Purpose of using Tandora')

    @transaction.atomic
    def handle(self, *args, **options):
        email = options.get('email')
        name = options.get('name')
        password = options.get('password')
        company_name = options.get('company_name')
        website = options.get('website')
        terminology = options.get('changelog_terminology', CHANGELOG_TERMINOLOGY)
        referral_code = options.get('referral_code')
        use_case = options.get('use_case')

        if use_case == 's' and terminology == CHANGELOG_TERMINOLOGY:
            terminology = 'website'

        arguments = [
            email,
            name,
            password,
            company_name,
            website,
            terminology,
            use_case,
        ]
        if not all(arguments):
            raise AssertionError("All required arguments are not present.")

        self.stdout.write("Creating company ..")

        data = {
            'company_name': company_name,
            'website': website,
            'changelog_terminology': terminology,
            'use_case': use_case,
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
        initial_data_json = current_path / 'initial_data_for_changelog.json'
        if use_case == 's':
            initial_data_json = current_path / 'initial_data_for_static_site.json'

        with open(initial_data_json) as initial_data:
            data = json.loads(initial_data.read())

            categories = list()
            for category in data['categories']:
                category['company'] = company
                categories.append(Category(**category))

            Category.objects.bulk_create(categories)

            if use_case == 'c':
                new_category = Category.objects.get(company=company, name='New')

                for changelog in data['changelogs']:
                    create_changelog(changelog, new_category, company)
            else:
                for changelog in data['changelogs']:
                    try:
                        category = Category.objects.get(company=company, name__iexact=changelog['title'])
                        content_file = changelog['title'].lower().replace(' ', '_') + '.txt'
                        content = ''
                        with open(current_path / content_file) as cf:
                            content = cf.read()
                        content = content.replace('Website Name', company.company_name)
                        content = content.replace('Company Name', company.company_name)
                        content = content.replace('Email@Website.com', company.admin.email)
                        content = content.replace('www.website.com', company.website)
                        content = content.replace('Website.com', company.website)
                        changelog['content'] = content
                        create_changelog(changelog, category, company)
                    except Category.DoesNotExist:
                        raise RuntimeError('Category does not exist.')

        if referral_code:
            try:
                referral = Referral.objects.get(referral_code=referral_code)
                referral.add_signup(company.id)
            except Referral.DoesNotExist:
                pass

        success_data = {
            'company_id': company.id,
        }

        self.stdout.write(f"Done creating company .. {success_data}", style_func=self.style.SUCCESS)
