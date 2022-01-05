from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.files.base import ContentFile
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.decorators.http import require_POST

from sorl.thumbnail import get_thumbnail, delete

from .forms import PostCreateForm, PostUpdateForm, CommentForm, PictureFormset, CommentDeleteForm, \
    MultiplePictureCreateForm
from .models import Post, Like, Comment, Picture
from myAccount.models import Relationship

import logging

application_logger = logging.getLogger('application-logger')

User = get_user_model()


def only_post_owner(user):
    return user.id in user.post_set.all().values_list('pk', flat=True)


class OnlyPostOwnerMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return self.kwargs['pk'] in user.post_set.all().values_list('pk', flat=True)


class PrivatePostListUserPassesTestMixin(UserPassesTestMixin):
    """遷移先のユーザーとリクエストユーザーが同じかどうか"""
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return self.kwargs['pk'] == user.pk


class PrivatePostDetailUserPassesTestMixin(UserPassesTestMixin):
    """遷移先のユーザーとリクエストユーザーが同じかどうか"""
    raise_exception = True

    def test_func(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        rtn = True
        if post.owner != user and not post.is_publish:
            rtn = False
        return rtn


# class Home(LoginRequiredMixin, generic.ListView):
#     """ホーム画面は全pictureをランダムに敷き詰めたデザイン"""
#     model = Picture
#     template_name = 'myProject/home.html'
#     ordering = '?'  # order_byの引数を'?'とするとランダムな順番のレコードを取得できる
#
#     def get_queryset(self):
#         # application_logger.debug('queryset取得')
#         queryset = Picture.objects.filter(post__is_publish=True).order_by('?')
#         return queryset


# @login_required
# def post_picture_create2(request):
#     """
#     新規投稿ビュー。
#     今後、投稿に対して複数枚アップできるようにpost本体とpictureでモデルを分けている。
#     そのため二つのモデルフォーム扱えるよう関数ベースで実装。
#     """
#     post_form = PostCreateForm(request.POST or None)
#     picture_form = MultiplePictureCreateForm(request.POST or None, request.FILES or None)
#
#     context = {
#         'post_form': post_form,
#         'picture_form': picture_form,
#     }
#
#     if request.method == 'POST':
#         if post_form.is_valid() and picture_form.is_valid():
#             post = post_form.save(commit=False)
#             post.owner = request.user
#             post.save()
#             multiple_picture = request.FILES.getlist('picture')
#             for picture in multiple_picture:
#                 instance = Picture(picture=picture, post=post, user=request.user)
#                 instance.save()
#             messages.success(request, '新規投稿しました')
#             # picture = picture_form.save(commit=False)
#             # picture.post = post
#             # picture.save()
#             return redirect('board:post_list')
#         else:
#             messages.warning(request, 'ERROR!!')
#             context['post_form'] = post_form
#             context['picture_form'] = picture_form
#
#     return render(request, 'board/post_create.html', context)


def post_picture_create(request):
    """新規投稿ビュー。画像を複数投稿するためにインラインフォームセットを利用している。"""
    post_form = PostCreateForm(request.POST or None)
    context = {'post_form': post_form}
    # success_url = 'board:post_list'
    success_url = reverse_lazy('myAccount:user_detail', kwargs={'pk': request.user.pk})
    success_message = '新規投稿しました'
    # print('*' * 100)
    # print(request.META.get('REMOTE_ADDR'))

    if request.method == 'POST' and post_form.is_valid():
        post = post_form.save(commit=False)
        post.owner = request.user
        picture_formset = PictureFormset(request.POST, files=request.FILES, instance=post, )
        if picture_formset.is_valid():

            if 'btn-draft' in request.POST:
                post.is_publish = False
                success_message = '下書き・非公開記事を作成しました'
                success_url = reverse('board:private_post_list', kwargs={'pk': request.user.pk})

            post.save()
            # commit=Falseの場合、削除チェックがついたpictureを取り出して手動で削除する必要あり
            pictures = picture_formset.save(commit=False)
            for picture in picture_formset.deleted_objects:
                picture.delete()

            # saveも個別に行う。
            for picture in pictures:
                picture.user = request.user
                picture.save()

            messages.success(request, success_message)
            return redirect(success_url)
        else:
            context['formset'] = picture_formset

    else:
        picture_formset = PictureFormset()
        context['formset'] = picture_formset

    # print(picture_formset.error_messages)
    return render(request, 'board/post_create.html', context)


class PostList(LoginRequiredMixin, generic.ListView):
    """投稿一覧ビュー。フォローしているユーザー限定のフィードを表示する。"""

    model = Post
    # paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'board/home_post_list.html'
    # ordering = '-updated_at'
    """
    orderingはget_queryset()の中でget_ordering()によって参照されている。
    なので、自前でget_queryset()を定義する場合は適用されず、order_byする必要がある。
    """

    def get_queryset(self, **kwargs):
        my_following_list = Relationship.objects.filter(following=self.request.user).values_list('followed_id',
                                                                                                 flat=True)
        post = self.model
        queryset = post.objects.filter(owner_id__in=my_following_list, is_publish=True).order_by('-updated_at')  # 一覧をフォローしてる人に絞り込む
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        post = self.model
        # flat=Trueでリスト型にしないと(タプルのままだと)、いいねの表示がうまくいかない
        liked_list = Like.objects.filter(user=user).values_list('post_id', flat=True)
        context['liked_list'] = liked_list
        return context


class PrivatePostList(PrivatePostListUserPassesTestMixin, LoginRequiredMixin, generic.ListView):

    model = Post
    context_object_name = 'private_post_list'
    template_name = 'board/private_post.html'

    def get_queryset(self, **kwargs):
        # my_following_list = Relationship.objects.filter(following=self.request.user).values_list('followed_id',
        #                                                                                          flat=True)
        post = self.model
        queryset = post.objects.filter(owner_id=self.kwargs['pk'], is_publish=False).order_by('-updated_at')  # 非公開記事に絞り込む
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        post = self.model
        # flat=Trueでリスト型にしないと(タプルのままだと)、いいねの表示がうまくいかない
        liked_list = Like.objects.filter(user=user).values_list('post_id', flat=True)
        context['liked_list'] = liked_list
        return context


class LikePostList(LoginRequiredMixin, generic.ListView):
    """ユーザーがいいねした投稿の一覧"""
    model = Post
    template_name = 'board/like_post_list.html'
    context_object_name = 'like_post_list'

    def get_queryset(self, **kwargs):
        # my_following_list = Relationship.objects.filter(following=self.request.user).values_list('followed_id',
        #                                                                                          flat=True)
        user = self.request.user
        post = self.model
        user_like_list = Like.objects.filter(user=user).values_list('post_id', flat=True)
        queryset = post.objects.filter(is_publish=True, pk__in=user_like_list).order_by('-updated_at')
        # queryset = post.objects.filter(is_publish=True, like).order_by('-updated_at')  # 非公開記事に絞り込む
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # flat=Trueでリスト型にしないと(タプルのままだと)、いいねの表示がうまくいかない
        liked_list = Like.objects.filter(user=user).values_list('post_id', flat=True)
        context['liked_list'] = liked_list
        return context





# def post_detail_and_comments(request, post_id):
#     print(vars(request))
#     post = get_object_or_404(Post, id=post_id)
#     comments = Comment.objects.filter(post=post).order_by('-created_at')
#     liked_list = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
#
#     if request.method == "POST":
#         form = CommentForm(request.POST or None)
#         if form.is_valid():
#             text = request.POST.get('text')
#             comment = Comment.objects.create(post=post, user=request.user, text=text)
#             comment.save()
#     else:
#         form = CommentForm()
#
#     context = {
#         'post': post,
#         'comments': comments,
#         'form': form,
#         'likes_list': liked_list,
#     }
#
#     if request.is_ajax():
#         html = render_to_string('board/comments.html', context, request=request)
#         return JsonResponse({'form': html})
#     return render(request, 'board/post_detail.html', context=context)


class PostDetailAndComments(PrivatePostDetailUserPassesTestMixin, LoginRequiredMixin, generic.DetailView):
    """
    投稿詳細と、それに対するコメントのビュー
    投稿が非公開の場合は投稿主以外アクセス不可
    """

    model = Post
    template_name = 'board/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        liked_list = Like.objects.filter(user=user).values_list('post_id', flat=True)
        context['liked_list'] = liked_list
        # postに紐づく画像を取得
        # レコードが一件であっても返されるのはクエリセット(リスト)なので、テンプレートでは{% for pic in pictures%}とする必要あり
        pictures = Picture.objects.filter(post=self.object).order_by('pk')
        context['pictures'] = pictures
        # GETメソッド内で呼ばれたget_object()でself.objectとしてPostオブジェクトが格納されている。
        comments = Comment.objects.filter(post=self.object).order_by('-created_at')
        context['comments'] = comments
        return context

    # def post(self, request, *args, **kwargs):
    #     # form_valid()内で紐づけるためにPost(投稿)オブジェクトを取得する。
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)
    #
    # def form_valid(self, form):
    #     instance = form.save(commit=False)
    #     instance.user = self.request.user
    #     instance.post = self.object
    #     instance.save()
    #     return super(PostDetail, self).form_valid(form)


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    # picture_list = Picture.objects.filter(post_id=pk)

    # 投稿者以外アクセス不可
    if user != post.owner:
        raise PermissionDenied

    post_form = PostCreateForm(request.POST or None, instance=post)
    formset = PictureFormset(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST' and post_form.is_valid() and formset.is_valid():

        if 'btn-draft' in request.POST:
            post_form.save()
            post = Post.objects.get(pk=pk)
            post.is_publish = False
            post.save()
        elif 'btn-publish' in request.POST:
            post_form.save()
            post = Post.objects.get(pk=pk)
            post.is_publish = True
            post.save()
        # commit=Falseの場合、削除チェックがついたpictureを取り出して手動で削除する必要あり
        pictures = formset.save(commit=False)
        for picture in formset.deleted_objects:
            picture.delete()
        # saveも個別に行う。
        for picture in pictures:
            # Picture.objects.filter(pk=picture.pk).update(picture=picture.picture.name)
            picture.user = user
            picture.save()
        messages.success(request, '投稿を編集しました')
        return redirect('board:post_detail', pk=pk)

    context = {
        # 'post': post,
        # 'picture_list': picture_list,
        'post_form': post_form,
        'formset': formset,
    }
    return render(request, 'board/post_update.html', context)


# def post_update_2(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     user = request.user
#     # 投稿者以外アクセス不可
#     if user != post.owner:
#         raise PermissionDenied
#
#     picture_list = Picture.objects.filter(post_id=pk)
#
#     post_form = PostCreateForm(request.POST or None, instance=post)
#     picture_form = MultiplePictureCreateForm(
#         request.POST or None, request.FILES or None,
#     )
#
#     if request.method == 'POST':
#         if post_form.is_valid() and picture_form.is_valid():
#             # post = post_form.save(commit=False)
#             # post.owner = request.user
#             post.save()
#             Picture.objects.filter(post=post).delete()
#             multiple_picture = request.FILES.getlist('picture')
#             for picture in multiple_picture:
#                 instance = Picture(picture=picture, post=post, user=request.user)
#                 instance.save()
#             messages.success(request, 'SUCCESS!!')
#
#             return redirect('board:post_list')
#
#     context = {
#         'post': post,
#         'picture_list': picture_list,
#         'post_form': post_form,
#         'picture_form': picture_form,
#     }
#
#     return render(request, 'board/post_update2.html', context)


class PostDelete(LoginRequiredMixin, OnlyPostOwnerMixin, SuccessMessageMixin, generic.DeleteView):
    """投稿削除"""

    model = Post
    template_name = 'board/post_delete.html'

    # deleteviewでは、SuccessMessageMixinが使われないので設定する必要あり
    # success_url = reverse_lazy('board:post_list')
    success_message = "投稿を削除しました。"

    def get_success_url(self):
        success_url = reverse('myAccount:user_detail', kwargs={'pk': self.request.user.pk})
        return success_url

    # 削除された際にメッセージが表示されるようにする。
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PostDelete, self).delete(request, *args, **kwargs)


@require_POST
@login_required
def add_or_del_like(request):
    """いいねボタン"""

    # print(vars(request))
    context = {}
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=request.POST.get('post_id'))
        user = request.user
        liked = False
        like = Like.objects.filter(post=post, user=user)

        if like.exists():
            like.delete()
        else:
            like.create(post=post, user=user)
            liked = True

        context = {
            'post_id': post.id,
            'liked': liked,
            'like_count': post.like_set.count()
        }

    if request.is_ajax():
        return JsonResponse(context)


@require_POST
@login_required
def comment(request):
    """投稿に対するコメント"""

    context = {}

    if request.method == 'POST':
        post = get_object_or_404(Post, pk=request.POST.get('post_id'))
        # post = get_object_or_404(Post, id=pk)
        form = CommentForm(request.POST or None)
        if form.is_valid():
            text = request.POST.get('text')
            Comment.objects.create(text=text, post=post, user=request.user)

            form = CommentForm()
            comments = Comment.objects.filter(post=post).order_by('-created_at')

            context = {
                'comments': comments,
                'post': post,
                'form': form,
            }

    if request.is_ajax():
        html = render_to_string('board/comments.html', context, request=request)
        return JsonResponse({'form': html})


@require_POST
@login_required
def ajax_comment_delete(request):
    context = {}

    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=request.POST.get('comment_id'))
        post = get_object_or_404(Post, pk=request.POST.get('post_id'))
        delete_form = CommentDeleteForm(request.POST or None)
        if delete_form.is_valid():
            comment.delete()
            # messages.success(request, 'コメントを削除しました')
            form = CommentForm()
            comments = Comment.objects.filter(post=post).order_by('-created_at')

            context = {
                'comments': comments,
                'post': post,
                'form': form,
            }

    if request.is_ajax():
        html = render_to_string('board/comments.html', context, request=request)
        return JsonResponse({'form': html})


def paginate_queryset(request, queryset, count):
    """Pageオブジェクトを返す。

    ページングしたい場合に利用してください。

    countは、1ページに表示する件数です。
    返却するPgaeオブジェクトは、以下のような感じで使えます。

        {% if page_obj.has_previous %}
          <a href="?page={{ page_obj.previous_page_number }}">Prev</a>
        {% endif %}

    また、page_obj.object_list で、count件数分の絞り込まれたquerysetが取得できます。

    """
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


def ajax_post_search(request):
    """投稿検索"""

    keyword = request.GET.get('content')

    """kwがあれば本文にひっかかるPostを。なければ全件をcontent_listに"""
    if keyword:
        search_result = [post for post in Post.objects.filter(content__icontains=keyword)]
    else:
        search_result = [post for post in Post.objects.all()]

    # page_obj = paginate_queryset(request, search_result, 2)
    liked_list = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    context = {
        'post_list': search_result,
        # 'post_list': page_obj.object_list,
        # 'page_obj': page_obj,
        'liked_list': liked_list,
    }

    if request.is_ajax():
        html = render_to_string('board/post_list_contents.html', context=context, request=request)
        return JsonResponse({'html': html})