from django.utils.translation import ugettext as _

CHANGELOG_CREATED_OR_EDITED_SUCCESSFULLY = _("Changelog {} success.")
CHANGELOG_DOES_NOT_EXIST_ERROR = _("Changelog does not exist.")
CHANGELOG_DELETED_SUCCESSFULLY = _("Changelog delete success.")

NOT_LOGGED_IN_ERROR = _("Please login to continue")

CATEGORY_CREATED_OR_EDITED_SUCCESSFULLY = _('Successfully {} category: {}')
CATEGORY_DELETED_SUCCESSFULLY = _('Category delete success.')
CATEGORY_DOES_NOT_EXIST = _('Category does not exist.')

COMPANY_CREATED_OR_EDITED_SUCCESSFULLY = _(
    'Successfully {} company: {}. As a security measure, you should log in again..')
COMPANY_DOES_NOT_EXIST = _('Company does not exist')

WIDGET_CREATED_OR_EDITED_SUCCESSFULLY = _('Successfully {} widget: {}')
WIDGET_DOES_NOT_EXIST = _('Widget does not exist')
WIDGET_CODE_EDIT_WARNING = _(
    'Please be cautious while editing this code as it can modify the appearance of widget.')
WIDGET_CSS_EDIT_WARNING = '// Please be cautious while editing this code as it can modify the appearance of widget.'

FREE_TRIAL_PERIOD_IN_DAYS = 7
PAYMENT_LINK = 'https://rzp.io/l/Iu3JAsJ'
UPGRADE = _(f'<a href="{PAYMENT_LINK}">Click here</a> to upgrade.')
FREE_TRIAL_EXPIRED = _(f'Your free trial is expired. {UPGRADE}')
LOGIN_AGAIN_INFO = _('Please login again to continue.')
TRIAL_UPGRADE_WARNING = _('Your trial ends in {days} days. ') + UPGRADE
TRIAL_ENDS_TODAY = _(f'Today is your last day of free trial. {UPGRADE}')
