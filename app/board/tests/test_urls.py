from django.test import TestCase
from django.urls import resolve, Resolver404

from ..views import (
    Home, PostList, LikePostList, PrivatePostList, PostDetailAndComments,
    post_picture_create, post_update, PostDelete, add_or_del_like, comment,
    ajax_comment_delete,
)

from ..models import Post, Picture


class TestUrls(TestCase):

    def test_not_exist_url(self):
        with self.assertRaises(Resolver404):
            resolve('/board/post/notexist')

    def test_home_url_is_exist(self):
        view = resolve('/board/home')
        self.assertEqual(view.func.view_class, Home)

    def test_list_url_is_exist(self):
        view = resolve('/board/post/list')
        self.assertEqual(view.func.view_class, PostList)

    def test_like_post_list_url_is_exist(self):
        view = resolve('/board/post/list/like')
        self.assertEqual(view.func.view_class, LikePostList)

    def test_private_post_list_is_exist(self):
        view = resolve('/board/post/list/1/private')
        self.assertEqual(view.func.view_class, PrivatePostList)

    def test_post_detail_url_is_exist(self):
        view = resolve('/board/post/1/detail')
        self.assertEqual(view.func.view_class, PostDetailAndComments)

    def test_post_create_url_is_exist(self):
        view = resolve('/board/post/create')
        """FBVはview.func"""
        self.assertEqual(view.func, post_picture_create)

    def test_post_update_url_is_exist(self):
        view = resolve('/board/post/1/update')
        self.assertEqual(view.func, post_update)

    def test_post_delete_url_is_exist(self):
        view = resolve('/board/post/1/delete')
        self.assertEqual(view.func.view_class, PostDelete)

    def test_like_url_is_exist(self):
        view = resolve('/board/like')
        """FBVはview.func"""
        self.assertEqual(view.func, add_or_del_like)

    def test_comment_url_is_exist(self):
        view = resolve('/board/comment')
        """FBVはview.func"""
        self.assertEqual(view.func, comment)

    def test_comment_delete_url_is_exist(self):
        view = resolve('/board/comment/delete')
        """FBVはview.func"""
        self.assertEqual(view.func, ajax_comment_delete)