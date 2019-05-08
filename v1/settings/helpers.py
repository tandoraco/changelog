from v1.accounts.models import User, Company
from v1.categories.models import Category
from v1.settings.public_page.models import PublicPage


def get_user(email):
    user = User.objects.get(email__iexact=email)

    return {
        'name': user.name,
        'email': user.email
    }


def get_company():
    company = Company.objects.get()

    return {
        'admin': company.admin.email,
        'website': company.website,
        'company_name': company.company_name,
        'terminology': company.changelog_terminology
    }


def get_public_page():
    public_page = PublicPage.objects.get()

    return {
        'color': public_page.color,
        'hide_from_crawlers': public_page.hide_from_crawlers,
        'show_authors': public_page.show_authors,
        'private_mode': public_page.private_mode
    }


def get_categories():
    categories = Category.objects.all()

    return [
        {
            'name': category.name,
            'color': category.color
        }
        for category in categories
    ]
