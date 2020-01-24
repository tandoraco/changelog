from django.utils.translation import ugettext as _


MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 15

MAX_EMAIL_LENGTH = 254

EMAIL_NOT_FOUND_ERROR = _("Email id is invalid.")
INACTIVE_USER_ERROR = _('Your account is not active. Please contact your company administrator.')
PASSWORD_INCORRECT_ERROR = _("Incorrect password.")
PASSWORD_LENGTH_VALIDATION_FAILED = _("Password length should be between {}-{} characters.".format(
    MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH))
PASSWORD_CONSTRAINS_NOT_MET = _("""Password should contain atleast one uppercase, one lowercase,
 one digit and one special character.""")
EMAIL_OR_PASSWORD_INVALID = _("Email or Password is invalid.")
SPECIAL_CHARACTERS_NOT_ALLOWED = _('Special characters are not allowed for this field.')

CHANGELOG_TERMINOLOGY = _("Changelog")

RESET_TOKEN_INVALID = _("Forgot password token is invalid.")

USE_CASE_CHOICES = (
    ('c', 'Tandora Changelog',),
    ('s', 'Tandora Web builder'),
)
