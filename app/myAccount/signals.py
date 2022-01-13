from allauth.account.models import EmailAddress
from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from django.db.models import signals

from .models import Relationship, Activity
from board.models import Comment


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = email_address.user
    old_email = EmailAddress.objects.filter(user=user).exclude(email=email_address.email)
    if old_email.exists():
        user.email = email_address.email
        user.save()
        email_address.primary = True
        email_address.save()
        old_email.delete()
    else:
        pass


@receiver(signal=signals.post_save, sender=Relationship)
def relationship_add_activity(sender, instance, **kwargs):
    activity = Activity(user=instance.followed, action_user=instance.following, activity=30, model_key=instance.pk)
    activity.save()