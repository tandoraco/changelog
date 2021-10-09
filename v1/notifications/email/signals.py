from django.db import transaction
from v1.notifications.email import core as email_core, events as email_events


@transaction.atomic
def send_user_verification_email(sender, instance, created, **kwargs):
    if created:
        from v1.accounts.models import PendingUser
        pending_user = PendingUser.objects.create(user=instance)
        email_core.NotificationCenter.handle(email_events.EVENT_USER_VERIFICATION, pending_user)


def send_forgot_password_mail(sender, instance, created, **kwargs):
    if created:
        email_core.NotificationCenter.handle(email_events.EVENT_FORGOT_PASSWORD, instance)
