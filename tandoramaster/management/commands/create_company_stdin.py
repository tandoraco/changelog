from getpass import getpass

from django.core.management import BaseCommand, call_command


class Command(BaseCommand):

    def handle(self, *args, **options):
        email = input("Email: ").strip()

        password = getpass("Password: ").strip()
        confirm_password = getpass("Confirm Password: ").strip()
        while password != confirm_password:
            self.stderr.write("Passwords does not match", style_func=self.style.ERROR)
            confirm_password = getpass("Confirm Password: ").strip()

        name = input('Name: ').strip()
        company_name = input('Company name: ').strip()
        website = input('Website: ').strip()
        changelog_terminology = input('Changelog Terminology: ').strip()
        use_case = input('Use case: either s or c:').strip().lower()

        call_command('create_company',
                     f'--email={email}',
                     f'--name={name}',
                     f'--password={password}',
                     f'--company_name={company_name}',
                     f'--website={website}',
                     f'--changelog_terminology={changelog_terminology}'
                     f'--use_case={use_case}'
                     )
