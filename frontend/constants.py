from django.utils.translation import ugettext as _

CHANGELOG_CREATED_OR_EDITED_SUCCESSFULLY = _("Changelog {} success.")
CHANGELOG_DOES_NOT_EXIST_ERROR = _("Changelog does not exist.")
CHANGELOG_DELETED_SUCCESSFULLY = _("Changelog delete success.")

NOT_LOGGED_IN_ERROR = _("Please login to continue")

CATEGORY_CREATED_OR_EDITED_SUCCESSFULLY = _('Successfully {} category: {}')
CATEGORY_DELETED_SUCCESSFULLY = _('Category delete success.')
CATEGORY_DOES_NOT_EXIST = _('Category does not exist.')

LINK_CREATED_SUCCESSFULLY = _("Link created successfully.")
LINK_DELETED_SUCCESSFULLY = _('Link deleted successfully.')
LINK_DOES_NOT_EXIST = _('Link not found.')


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

PASSWORD_RESET_INITIATED = _('You will receive an email with instructions to reset the password.')
PASSWORD_DOES_NOT_MATCH = _('Passwords does not match.')
PASSWORD_RESET_SUCCESS = _('Your password is reset successfully.')
PASSWORD_RESET_TOKEN_INVALID = _('Reset password link is expired or does not exist. Please initiate a new request.')

EMAIL_EXISTS_ERROR = _('Email is already present in our records. Please enter a different email.')
WEBSITE_EXISTS_ERROR = _('Website is already present in our records. Please enter a different website.')

ACCOUNT_CREATED_MESSAGE = _('Your account is created. Check your email for instructions to verify your account.')
AFFILIATE_CREATED_SUCCESSFULLY = _('Your request is received. We will contact you shortly.')
INVALID_REFERRAL_CODE = _('Invalid referral code.')

NOT_ALLOWED = _('Not allowed for this plan.')
THEME_SET_SUCCESS = _('Theme for Website set successfully.')

PLAN_LIMIT_REACHED_MESSAGE = _('You cannot perform this action, since the plan limit is reached. Contact support.')

USER_VERIFICATION_FAILED = _('Your account is either verified or the verification link is expired.')
USER_VERIFICATION_SUCCESS = _('Your account is successfully verified. Please login.')

ONLY_ADMIN_CAN_PERFORM_THIS_ACTION_ERROR = _('Only the company administrator can perform this action.')

USER_CREATED_OR_EDITED_SUCCESSFULLY = _('Successfully {} user: {}')
USER_DELETED_SUCCESSFULLY = _('User delete success.')
USER_DOES_NOT_EXIST = _('User does not exist.')
USER_DEACTIVATED_SUCCESSFULLY = _('User deactivation success.')
USER_ACTIVATED_SUCCESSFULLY = _('User activation success.')

INTEGRATION_NOT_AVAILABLE_FOR_PLAN_ERROR = "Your current subscription plan does not allow this integration." \
                                           "Please contact support@tandora.co for more details. "
INTEGRATION_EDITED_SUCCESSFULLY = _("Integration updated successfully.")
INTEGRATION_EDIT_FAILED_ERROR = _("Integration editing failed. Please try again after some time.")

WEB_BUILDER_SETUP_COMPLETED_PREVIEW_WEBSITE_MESSAGE = _(
    'You have successfully completed website setup. Click <a target="_blank" '
    'href="url">here</a> to view preview of website.')

PUBLIC_PAGE_CHANGELOG_10_MULTIPLE_ERROR = _('This value should be a multiple of 10.')


SLACK_INSTALLATION_SUCCESS = _('Slack was installed successfully.')
SLACK_INSTALLATION_FAILED = _('Unable to install Slack. Please try again.')
