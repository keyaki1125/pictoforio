from django.contrib.auth import get_user_model
from django.db.models import signals
from django.dispatch import receiver

from myAccount.models import Activity, Relationship, MyUser
from .models import Post, Like, Comment


@receiver(signal=signals.post_save, sender=Like)
def like_add_activity(sender, instance, **kwargs):
    print('like!!')
    activity = Activity(user=instance.post.owner, action_user=instance.user, activity=10, model_key=instance.post.pk)
    activity.save()


@receiver(signal=signals.post_save, sender=Comment)
def comment_add_activity(sender, instance, **kwargs):
    print('comment!!')
    activity = Activity(user=instance.post.owner, action_user=instance.user, activity=20, model_key=instance.post.pk)
    activity.save()