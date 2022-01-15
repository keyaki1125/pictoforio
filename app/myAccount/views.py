import base64
import os
import random
import string
import uuid

from allauth.account.views import EmailView, PasswordChangeView, PasswordResetView
import boto3
import cv2
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.decorators.http import require_POST, require_GET
from django_cleanup import cleanup
import numpy as np

from .forms import ProfileForm, MyResetPasswordForm
from .models import Relationship, Activity
from board.models import Post, Comment, Like, Picture

User = get_user_model()


class GuestUserPermissionMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return not user.is_guest


class UserList(LoginRequiredMixin, generic.ListView):
    """ユーザ一覧"""

    template_name = 'account/user_list.html'
    model = User

    def get_queryset(self):
        User = self.model
        qs = User.objects.exclude(pk=self.request.user.pk)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        my_follow_list = Relationship.objects.filter(following=user).values_list('followed_id', flat=True)
        my_follows = User.objects.filter(id__in=my_follow_list)
        context['my_follows'] = my_follows
        # context['picture_count'] = Picture.objects.filter(user=user).count()
        return context


class UserDetail(LoginRequiredMixin, generic.DetailView):
    """ユーザ詳細。ログインユーザであれば編集ボタンを、それ以外であればフォローボタンを表示する。"""

    template_name = 'account/base_user_page.html'
    model = User
    context_object_name = 'target_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = Post.objects.filter(owner=self.object, is_publish=True).order_by('-updated_at')
        context['liked_list'] = Like.objects.filter(user=self.object).values_list('post_id', flat=True)

        target_user_follow_list = Relationship.objects.filter(following=self.object).values_list('followed_id', flat=True)
        context['target_user_follows'] = User.objects.filter(id__in=target_user_follow_list)

        target_user_followers_list = Relationship.objects.filter(followed=self.object).values_list('following_id', flat=True)
        context['target_user_followers'] = User.objects.filter(pk__in=target_user_followers_list)

        my_follow_list = Relationship.objects.filter(following=self.request.user).values_list('followed_id', flat=True)
        context['my_follows'] = User.objects.filter(pk__in=my_follow_list)

        return context


class UserPictureList(LoginRequiredMixin, generic.ListView):

    template_name = 'account/picture_list.html'
    model = Picture

    def get_queryset(self):
        queryset = Picture.objects.filter(user__id=self.kwargs['pk']).order_by('-created_at')
        return queryset


class ProfileEdit(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    """プロフィール編集ビュー"""

    template_name = 'account/edit_profile.html'
    model = User
    form_class = ProfileForm
    success_message = 'プロフィールを編集しました'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse('myAccount:user_detail', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        """コンテキストとして渡すユーザーオブジェクトをリクエストユーザに指定する。
        (URLconfでpkのパラメータを渡さなくてよくなる)"""
        return self.request.user


# class MyProfile(LoginRequiredMixin, generic.ListView):
#     template_name = 'account/base_my_page.html'
#     model = Post
#     context_object_name = 'post_list'
#     # paginate_by = 3
#
#     def get_queryset(self):
#         query_set = Post.objects.filter(owner=self.request.user)
#         return query_set
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         liked_list = Like.objects.filter(user=user).values_list('post_id', flat=True)
#         context['liked_list'] = liked_list
#         my_follows_list = Relationship.objects.filter(following=user).values_list('followed_id')
#         my_follows = User.objects.filter(pk__in=my_follows_list)
#         my_followers_list = Relationship.objects.filter(followed=user).values_list('following_id')
#         my_followers = User.objects.filter(pk__in=my_followers_list)
#         context['my_follows'] = my_follows
#         context['my_followers'] = my_followers
#         return context


class MyEmailView(GuestUserPermissionMixin, LoginRequiredMixin, EmailView):
    # allauthのオーバーライド。ゲストユーザーのアクセス制限。
    pass


class MyPasswordChange(GuestUserPermissionMixin, LoginRequiredMixin, PasswordChangeView):
    """
    パスワード変更ビュー
    allauthで用意されているクラスのsuccess_urlをカスタムしている。
    ゲストユーザーのアクセス制限。
    """

    def get_success_url(self):
        success_url = reverse('myAccount:user_detail', kwargs={'pk': self.request.user.pk})
        return success_url


class MyPasswordReset(PasswordResetView):
    # allauthのオーバーライド。ゲストユーザーのアクセス制限。
    form_class = MyResetPasswordForm


@require_POST
@login_required
def profile_image_upload(request):
    """
    プロフィール画像アップロードビュー。
    croppieというjsライブラリを利用して画像をトリミングして登録する。
    画像を更新する場合は、前の画像は削除される。
    """
    user = request.user
    image_data = base64.b64decode(request.POST.get('image').split(',')[1])
    image_binary = np.frombuffer(image_data, dtype=np.uint8)
    image = cv2.imdecode(image_binary, cv2.IMREAD_COLOR)  # cv2でbase64を画像にデコード
    new_file_name = f'{str(uuid.uuid4())}.png'
    new_file_path = os.path.join('images', 'avatars', new_file_name)
    new_file_abspath = os.path.join(settings.BASE_DIR, 'media', new_file_path)
    cv2.imwrite(new_file_abspath, image)
    if settings.DEBUG:
        # 旧ファイルがあれば消す
        old_file_name = user.avatar.name
        if old_file_name or old_file_name != '':
            rm_old_file_path = os.path.join(settings.MEDIA_ROOT, old_file_name)
            try:
                os.remove(rm_old_file_path)
            except FileNotFoundError:
                pass
        # 新ファイルパス登録
        user.avatar = new_file_path
        user.save()
    else:
        # DEBUG=Falseならs3に保存する
        bucket_name = 'pictoforio'  # これは本番用のs3バケット
        s3_file_path = os.path.join('media', new_file_path)
        s3 = boto3.resource('s3')
        # 保存
        s3.Bucket(bucket_name).upload_file(Filename=new_file_abspath, Key=s3_file_path, ExtraArgs={"ContentType": "image/png"})
        # ローカルに保存したファイル削除
        os.remove(new_file_abspath)
        s3_root_path = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/media/'
        s3_full_path = os.path.join(s3_root_path, new_file_path)
        # 旧ファイルあれば消す
        old_file = user.avatar
        if old_file:
            client = boto3.client('s3')
            client.delete_object(Bucket=bucket_name, Key=user.avatar.url)
        # 新ファイルパス登録
        user.avatar = new_file_path
        user.save()

    if request.is_ajax():
        data = {'imageURL': user.avatar.url}
        return JsonResponse(data)


@require_POST
@login_required
def add_or_del_relationship(request):
    """フォローしたりされたりするビュー"""

    context = {}

    if request.method == 'POST':
        # フォローしてる側(= ログインユーザ)
        following = request.user
        # フォローされてる側(POSTパラメータの'followed_user_id')
        follow_target = get_object_or_404(User, pk=request.POST.get('follow_target_id'))
        relation = False
        relationship = Relationship.objects.filter(following_id=following.id, followed_id=follow_target.id)

        # すでにフォロー関係にあれば削除、無ければ新規作成
        if relationship.exists():
            relationship.delete()
        else:
            relationship.create(following_id=following.id, followed_id=follow_target.id)
            relation = True

        context = {
            'relation': relation,
            'follow_target_id': follow_target.id,
        }

    if request.is_ajax():
        return JsonResponse(context)


@require_POST
@login_required
def ajax_activity_watched(request):

    context = {}
    if request.method == 'POST':
        Activity.objects.filter(user=request.user).exclude(watched_flag=True).update(watched_flag=True)
        # print(activities)
        # activity_list = []
        #
        # if activities:
        #     for activity in activities:
        #         activity.watched_flag = True
        #         if activity.activity == 10:
        #             instance = Like.objects.get(pk=activity.model_key)
        #             activity_list.append(instance)
        #         elif activity.activity == 20:
        #             instance = Comment.objects.get(pk=activity.model_key)
        #             activity_list.append(instance)
        #         elif activity.activity == 30:
        #             instance = Relationship.objects.get(pk=activity.model_key)
        #             activity_list.append(instance)
        #
        # print(activity_list)
        # for activity in activities:
        # # 出来上がったらコメント解除する
        #     activity.watched_flag = True
        #     activity.save()

        # context['activities'] = {}
        # context['activity_list'] = activity_list

    if request.is_ajax():
        html = render_to_string('account/activity.html', context, request=request)
        return JsonResponse({'html': html})