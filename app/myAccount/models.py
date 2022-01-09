import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import get_thumbnail, delete


def image_directory_path(instance, filename):
    return f'images/avatars/{str(uuid.uuid4())}.{filename.split(".")[-1]}'


class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    nickname = models.CharField(_('nickname'), max_length=50, blank=True)
    introduce = models.TextField(verbose_name='自己紹介', blank=True, max_length=1024)
    avatar = models.ImageField(max_length=255, upload_to=image_directory_path, verbose_name='プロフィール画像', blank=True, null=True)

    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        # superuser作成時のためにデフォルトはTrueにしておく
        _('active'), default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    create_at = models.DateTimeField(auto_now_add=True)  # 追加時の日時を登録
    update_at = models.DateTimeField(auto_now=True)  # 追加、更新時の日時を登録

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    # def get_full_name(self):
    #     """Return the first_name plus the last_name, with a space in
    #     between."""
    #     # full_name = '%s %s' % (self.first_name, self.last_name)
    #     full_name = f'{self.first_name} {self.last_name}'
    #     return full_name.strip()
    #
    # def get_short_name(self):
    #     """Return the short name for the user."""
    #     return self.first_name

    # def save(self, *args, **kwargs):
    #     super(MyUser, self).save(*args, **kwargs)
    #     # 登録時はアバターは必須要素ではない
    #     if self.avatar:
    #         tmp_img_name = self.avatar.name
    #         if self.avatar.width > 500 or self.avatar.height > 500:
    #             new_width = 500
    #             new_height = 500
    #
    #             resized = get_thumbnail(self.avatar, f'{new_width}x{new_height}')
    #             name = resized.name.split('/')[-1]
    #             self.avatar.save(name, ContentFile(resized.read()), True)
    #
    #             try:
    #                 delete(tmp_img_name)
    #             except ObjectDoesNotExist as e:
    #                 print(e)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        return self.email

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_absolute_url(self):
        return reverse('myAccount:home')


class Relationship(models.Model):
    # フォローする側
    following = models.ForeignKey(MyUser, related_name='following', on_delete=models.CASCADE)
    # フォローされる側
    followed = models.ForeignKey(MyUser, related_name='followed', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['following', 'followed'],
                                    name='user-relationship')
        ]

    def __str__(self):
        return f'{self.following.username} : {self.followed.username}'


class Activity(models.Model):
    ACTIVITY_CHOICES = (
        (10, 'Like'),
        (20, 'Comment'),
        (30, 'Relationship'),
    )

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='me')
    action_user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='you')
    watched_flag = models.BooleanField(verbose_name='確認済ステータス', default=False)
    activity = models.IntegerField(choices=ACTIVITY_CHOICES, )
    model_key = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'activities'

    def __str__(self):
        return f'{self.get_activity_display()}ed : {self.action_user} → {self.user} : {self.timestamp}'