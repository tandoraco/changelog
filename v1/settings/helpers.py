from django.forms import model_to_dict

from v1.accounts.models import User
from v1.categories.models import Category
from v1.settings.public_page.models import PublicPage


def get_user(email):
    user = User.objects.get(email__iexact=email)

    return {
        'name': user.name,
        'email': user.email
    }


def get_company(company):

    return {
        'admin': company.admin.email,
        'website': company.website,
        'company_name': company.company_name,
        'terminology': company.changelog_terminology
    }


def get_public_page(company):
    public_page = PublicPage.objects.get(company=company)
    return model_to_dict(public_page, exclude=['id', ])


def get_categories(company):
    categories = Category.objects.filter(company=company)

    return [
        {
            'name': category.name,
            'color': category.color
        }
        for category in categories
    ]
