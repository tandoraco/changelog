import pytest
from faker import Faker

from v1.static_site.models import StaticSiteTheme, StaticSiteField, StaticSiteThemeConfig


@pytest.fixture
def theme(company):
    content = '<html><head>{{ title }}</head>'
    content += '<body>'
    content += '{{ home_page_content }}<br>'
    content += '{{ link }}<br>'
    content += '{{ email }}<br>'
    content += '{{ phone }}<br>'
    content += '</body>'
    content += '</html>'

    with pytest.raises(RuntimeError):
        # Either template file or content  is required to create theme.
        StaticSiteTheme.objects.create(name='test')

    return StaticSiteTheme.objects.create(name='test', template_content=content)


@pytest.fixture
def static_site_fields(company):
    _static_site_fields = [
        StaticSiteField(name='title', type='c', required=True),
        StaticSiteField(name='home_page_content', type='t'),
        StaticSiteField(name='email', type='e', required=True),
        StaticSiteField(name='phone', type='p'),
        StaticSiteField(name='link', type='l')
    ]

    return StaticSiteField.objects.bulk_create(_static_site_fields)


@pytest.fixture
def static_site_field_values():
    fake = Faker()
    return {
        'font': 'https://fonts.googleapis.com/css?family=Poppins&display=swap',
        'title': fake.name(),
        'home_page_content': fake.text(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'link': fake.url()
    }


@pytest.fixture
def static_site_config(company, theme, static_site_fields, static_site_field_values):
    config = StaticSiteThemeConfig.objects.create(theme=theme)
    for field in StaticSiteField.objects.all():
        config.fields.add(field)

    settings = company.settings
    settings['theme'] = theme.name
    settings['static_site_config'] = static_site_field_values
    company.settings = settings
    company.use_case = 's'
    company.save()

    return config
