from django.core.management import BaseCommand


class Command(BaseCommand):
    description = "Create a seperate database for a company."

    def add_arguments(self, parser):
        parser.add_argument('-e', '--email', type=str, help='Email address of company admin')
        parser.add_argument('-p', '--password', type=str, help='Password')
        parser.add_argument('-c', '--company_name', type=str, help='Company name')
        parser.add_argument('-w', '--website', type=str, help='Company website address')
        parser.add_argument('-ct', '--changelog_terminology', type=str, help='How the company wants to name changelog?')

    def handle(self, *args, **options):
        email = options.get('email')
        password = options.get('password')
        company_name = options.get('company_name')
        website = options.get('website')
        terminology = options.get('changelog_terminology')

        if not(email and password and company_name and website and terminology):
            raise AssertionError("All required arguments are not present.")
