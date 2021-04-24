from django.utils.translation import ugettext as _

CHANGELOG_PUBLISHED = 'pu'
NEW_CHANGELOG = 'ne'

CHANGELOG_PUBLISHED_TEXT = 'Whenever a changelog is published for the first time'
NEW_CHANGELOG_TEXT = 'Whenever a changelog is created whether it is published or not'

TRIGGER_CHOICES = (
    (CHANGELOG_PUBLISHED, _('Whenever a changelog is published for the first time')),
    (NEW_CHANGELOG, _('Whenever a changelog is created whether it is published or not'))
)
