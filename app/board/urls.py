from django.urls import path

from . import views

app_name = 'board'

urlpatterns = [
    # path('home', views.Home.as_view(), name='home'),
    path('post/list', views.PostList.as_view(), name='post_list'),
    path('post/list/like', views.LikePostList.as_view(), name='like_post_list'),
    path('post/list/<int:pk>/private', views.PrivatePostList.as_view(), name='private_post_list'),
    path('post/<int:pk>/detail', views.PostDetailAndComments.as_view(), name='post_detail'),
    path('post/create', views.post_picture_create, name='create'),
    path('post/<int:pk>/update', views.post_update, name='post_update'),
    path('post/<int:pk>/delete', views.PostDelete.as_view(), name='post_delete'),
    path('like', views.add_or_del_like, name='like'),
    path('comment', views.comment, name='comment'),
    path('comment/delete', views.ajax_comment_delete, name='comment_delete'),
    path('post/search', views.ajax_post_search, name='post_search'),
]