import random
import string

from django.core.management import BaseCommand

from v1.accounts.models import Referral


def get_random_referral_code():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(10))


class Command(BaseCommand):
    def handle(self, *args, **options):
        name = input('Enter base name: ').strip()
        n = int(input('Enter n: ').strip())

        referrals = []
        referral_codes = set()
        for i in range(n):
            ref_code = get_random_referral_code()
            referral_codes.add(ref_code)
            referrals.append(Referral(reference_name=f'{name}', referral_code=ref_code))

        created_referrals = Referral.objects.bulk_create(referrals)
        print(created_referrals)
