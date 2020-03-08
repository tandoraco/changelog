from django.conf import settings
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not settings.DEBUG:
            self.stderr.write("This command is allowed only in dev environment",
                              style_func=self.style.ERROR)

        data = {
            "email": "static@localhost.com",
            "password": "Static123.",
            "name": "Tandora Static",
            "company_name": "Tandora Dev Website",
            "website": "https://tandorawebsite.co",
            "changelog_terminology": "website",
            "use_case": "s",
        }

        call_command('create_company',
                     f'--email={data["email"]}',
                     f'--name={data["name"]}',
                     f'--password={data["password"]}',
                     f'--company_name={data["company_name"]}',
                     f'--website={data["website"]}',
                     f'--changelog_terminology={data["changelog_terminology"]}',
                     f'--use_case={data["use_case"]}',
                     )

        # Populate theme, fields and theme config
        call_command('load_static_site_data')
