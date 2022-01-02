import os
import uuid
from pprint import pprint

from django.conf import settings
from django.http import request

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myProject.settings')
from django import setup

setup()

from django.db import models
from django.contrib.auth import get_user_model
from myAccount.models import Relationship, MyUser
from board.models import Post, Like, Comment

from django.dispatch import receiver
from django.db.models import signals

User = get_user_model()

# @receiver(signal=signals.post_save, sender=Like)
# def like_add_activity(sender, instance, **kwargs):
#     activity = Activity(user=instance.post.owner, action_user=instance.user, activity=10, model_key=instance.pk)
#     activity.save()
#
# @receiver(signal=signals.post_save, sender=Comment)
# def comment_add_activity(sender, instance, **kwargs):
#     activity = Activity(user=instance.post.owner, action_user=instance.user, activity=20, model_key=instance.pk)
#     activity.save()
#
# @receiver(signal=signals.post_save, sender=Relationship)
# def comment_add_activity(sender, instance, **kwargs):
#     activity = Activity(user=instance.followed, action_user=instance.user, activity=20, model_key=instance.pk)
#     activity.save()

post1 = Post.objects.first()
# pprint(dir(post1))
print(str(post1.__class__))

# new_file_path = f'/images/avatars/{str(uuid.uuid4())}.png'
# file_name = f'{str(uuid.uuid4())}.png'
# new_file_path = os.path.join('images', 'avatars', file_name)
# print(new_file_path)
# abs_path = os.path.join(settings.MEDIA_ROOT, new_file_path)
# print(abs_path)
# # print(settings.MEDIA_ROOT)
# # print(settings.BASE_DIR)
#
#
#
# class Activity(models.Model):
#     ACTIVITY_CHOICES = (
#         (10, 'Like'),
#         (20, 'Comment'),
#         (30, 'Relationship'),
#     )
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='me')
#     action_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='you')
#     watched_flag = models.BooleanField(verbose_name='確認済ステータス', default=False)
#     activity = models.IntegerField(choices=ACTIVITY_CHOICES,)
#     model_key = models.IntegerField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         db_table = 'activities'
#
#     def __str__(self):
#         return f'{self.action_user} : {self.get_activity_display()}ed'

# activities = Activity.objects.filter(user=request.user).exclude(watched_flag=True)
#
# activity_list = []
#
# for activity in activities:
#     activity.watched_flag = True
#     if activity.activity == 10:
#         instance = Like.objects.get(pk=activity.model_key)
#         activity_list.append(instance)
#     elif activity.activity == 20:
#         instance = Comment.objects.get(pk=activity.model_key)
#         activity_list.append(instance)
#     elif activity.activity == 30:
#         instance = Relationship.objects.get(pk=activity.model_key)
#         activity_list.append(instance)