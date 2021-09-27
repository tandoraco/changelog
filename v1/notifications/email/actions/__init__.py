from django.conf import settings
from django.core.mail import send_mail


class EmailActionBase:

    def __init__(self, email_context):
        self.email_context = email_context

    def get_context(self):
        raise NotImplementedError

    def execute(self):
        context = self.get_context()
        from_email = settings.DEFAULT_FROM_EMAIL
        subject = context.get('subject')
        to = context.pop('to')

        '''if not settings.DEBUG:
            message = context.get('body')
        else:
            message = render_to_string('email/generic_email_template.html', context)'''
        message = context.get('body')

        # send_mail(subject, message, from_email, to, html_message=message)
        send_mail(subject, message, from_email, to)
