import subprocess
import sys

from django.core.management import BaseCommand

from tandora import settings
from tandoramaster.constants import CREATE_DB_COMMAND, CREATE_DB_COMMAND_WITH_PASSWORD
from tandoramaster.models import Company


class Command(BaseCommand):
    description = "Create a seperate database for a company."

    def add_arguments(self, parser):
        parser.add_argument('-e', '--email', type=str, help='Email address of company admin')
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

    def handle(self, *args, **options):
        email = options.get('email')
        password = options.get('password')
        company_name = options.get('company_name')
        website = options.get('website')
        terminology = options.get('changelog_terminology')
        subdomain = options.get('subdomain')

        if not(email and password and company_name and website and terminology and subdomain):
            raise AssertionError("All required arguments are not present.")
        db_name = f'tandora_{company_name}'

        try:
            Company.objects.get(subdomain=subdomain, db_name=db_name)
            # Todo send mail
            self.stderr.write('Subdomain and db exists', style_func=self.style.ERROR)
            sys.exit(0)
        except Company.DoesNotExist:
            pass

        self.create_db(db_name)

        Company.objects.create(name=company_name, email=email, db_name=db_name, subdomain=subdomain)
