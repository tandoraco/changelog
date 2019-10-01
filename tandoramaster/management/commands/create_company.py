import os
import pathlib
import subprocess
import sys
import tempfile
from datetime import datetime

import pytz
from django.core.management import BaseCommand, call_command
from django.db import transaction
from dynamic_db_router import in_database

from frontend.multidb.utils import add_instance_to_settings
from tandora import settings
from tandoramaster.constants import (CREATE_DB_COMMAND,
                                     CREATE_DB_COMMAND_WITH_PASSWORD,
                                     DELETE_DB_COMMAND_WITH_PASSWORD,
                                     DELETE_DB_COMMAND)
from tandoramaster.models import Instance
from v1.accounts.serializers import CompanySerializer


def get_current_utc_time():
    current_time = datetime.utcnow()
    return str(current_time.replace(tzinfo=pytz.utc))


class Command(BaseCommand):
    description = "Create a seperate database for a company."

    def add_arguments(self, parser):
        parser.add_argument('-e', '--email', type=str, help='Email address of company admin')
        parser.add_argument('-n', '--name', type=str, help='Admin name')
        parser.add_argument('-p', '--password', type=str, help='Password')
        parser.add_argument('-c', '--company_name', type=str, help='Company name')
        parser.add_argument('-w', '--website', type=str, help='Company website address')
        parser.add_argument('-ct', '--changelog_terminology', type=str, help='How the company wants to name changelog?')
        parser.add_argument('-sd', '--subdomain', type=str, help='Subdomain')

    def create_db(self, db_name):
        db = settings.DATABASES['default']

        if db.get('PASSWORD'):
            create_db = CREATE_DB_COMMAND_WITH_PASSWORD.format(username=db['USER'], host=db['HOST'],
                                                               database_name=db_name,
                                                               password=db['PASSWORD'])
        else:
            create_db = CREATE_DB_COMMAND.format(username=db['USER'], host=db['HOST'],
                                                 database_name=db_name)

        try:
            subprocess.run(create_db.split(' '), check=True, capture_output=True)
            self.stdout.write(f"Successfully created db {db_name}", style_func=self.style.SUCCESS)
        except subprocess.CalledProcessError as e:
            self.stderr.write("Error during create db", style_func=self.style.WARNING)
            self.stderr.write(e.__repr__(), style_func=self.style.WARNING)
            sys.exit(0)

    def drop_db(self, db_name):
        db = settings.DATABASES['default']

        if db.get('PASSWORD'):
            delete_db = DELETE_DB_COMMAND_WITH_PASSWORD.format(username=db['USER'], host=db['HOST'],
                                                               database_name=db_name,
                                                               password=db['PASSWORD'])
        else:
            delete_db = DELETE_DB_COMMAND.format(username=db['USER'], host=db['HOST'],
                                                 database_name=db_name)

        print(f"Delete this db using the command {delete_db}")

    @transaction.atomic
    def handle(self, *args, **options):
        email = options.get('email')
        name = options.get('name')
        password = options.get('password')
        company_name = options.get('company_name')
        website = options.get('website')
        terminology = options.get('changelog_terminology')
        subdomain = options.get('subdomain')

        if not (email and name and password and company_name and website and terminology and subdomain):
            raise AssertionError("All required arguments are not present.")
        db_name = f'tandora_{company_name}'

        try:
            Instance.objects.get(subdomain=subdomain, db_name=db_name)
            # Todo send mail
            self.stderr.write('Subdomain and db exists', style_func=self.style.ERROR)
            sys.exit(0)
        except Instance.DoesNotExist:
            pass

        self.create_db(db_name)

        db_user = settings.DATABASES['default']['USER']
        db_host = settings.DATABASES['default']['HOST']
        db_port = settings.DATABASES['default']['PORT']

        instance = Instance.objects.create(admin_name=company_name, email=email,
                                           db_name=db_name,
                                           db_user=db_user,
                                           db_password='',
                                           db_host=db_host,
                                           db_port=db_port,
                                           subdomain=subdomain)
        add_instance_to_settings(instance)

        with in_database(db_name, write=True):
            self.stdout.write(f"Running migrations for {db_name} ..")
            call_command('migrate', f'--database={db_name}')

            self.stdout.write(f"Creating admin ..")

            data = {
                'company_name': company_name,
                'website': website,
                'changelog_terminology': terminology,
                'email': email,
                'name': name,
                'password': password
            }

            company_serializer = CompanySerializer(data=data)
            if company_serializer.is_valid():
                company_serializer.save()
            else:
                self.stderr.write("Creating admin failed", style_func=self.style.ERROR)
                print(company_serializer.errors)
                self.drop_db(db_name)
                sys.exit(0)

            self.stdout.write(f"Populating initial data ..")

            current_path = pathlib.Path(__file__).parent
            initial_data_json = current_path / 'initial_data.json'

            temp_fixture_file = ''
            with tempfile.NamedTemporaryFile(suffix='.json', mode='w', delete=False) as temp_fixture:

                with open(initial_data_json) as initial_data:
                    data = initial_data.read()
                    data = data.replace('{created_time}', get_current_utc_time())
                    temp_fixture.write(data)

                temp_fixture_file = temp_fixture.name

            call_command('loaddata', temp_fixture_file, f'--database={db_name}')
            os.remove(temp_fixture_file)

            self.stdout.write(f"Done creating company ..", style_func=self.style.SUCCESS)
