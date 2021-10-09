from v1.notifications.email import events
from v1.notifications.email.actions.staff_account import ForgotPasswordAction, VerifyAccountAction
from v1.notifications.email.templates.json_templates import TEMPLATES


class NotificationCenter:

    @classmethod
    def handle(cls, event, *args, **kwargs):
        email_context = TEMPLATES.get(event, {})
        if event == events.EVENT_FORGOT_PASSWORD:
            cls.handle_forgot_password(email_context, *args, **kwargs)
        elif event == events.EVENT_USER_VERIFICATION:
            cls.handle_user_account_verification(email_context, *args, **kwargs)

    @staticmethod
    def handle_forgot_password(email_context, forgot_password):
        email_context['forgot_password'] = forgot_password
        ForgotPasswordAction(email_context).execute()

    @staticmethod
    def handle_user_account_verification(email_context, pending_user):
        email_context['pending_user'] = pending_user
        VerifyAccountAction(email_context).execute()
