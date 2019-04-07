from django.utils.translation import ugettext as _


MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 15

EMAIL_NOT_FOUND = _("Email id is invalid.")
PASSWORD_INCORRECT = _("Incorrect passoword.")
PASSWORD_LENGTH_VALIDATION_FAILED = _("Password length should be between {}-{} characters.".format(
    MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH))
PASSWORD_CONSTRAINS_NOT_MET = _("""Password should contain atleast one uppercase, one lowercase,
 one digit and one special character.""")
EMAIL_OR_PASSWORD_INVALID = _("Email or Password is invalid.")
