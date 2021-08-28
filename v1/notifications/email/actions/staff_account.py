from urllib.parse import urljoin

from django.conf import settings

from v1.notifications.email.actions import EmailActionBase


class ForgotPasswordAction(EmailActionBase):

    def get_context(self):
        forgot_password = self.email_context.pop('forgot_password')
        link = urljoin(settings.HOST, f'reset-password/{forgot_password.token}')
        body = self.email_context['body']
        body = body.format(**{'link': link})
        self.email_context['body'] = body
        self.email_context['to'] = [forgot_password.email]
        return self.email_context


class VerifyAccountAction(EmailActionBase):

    def get_context(self):
        pending_user = self.email_context.pop('pending_user')
        link = urljoin(settings.HOST, f'verify-user/{pending_user.uuid}')
        body = self.email_context['body']
        body = body.format(**{'link': link})
        self.email_context['body'] = body
        self.email_context['to'] = [pending_user.user.email]
        return self.email_context
