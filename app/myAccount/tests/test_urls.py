from django.test import TestCase
from django.urls import resolve, Resolver404

from ..views import (
    ProfileEdit, profile_image_upload, UserList, UserDetail, UserPictureList,
    add_or_del_relationship, ajax_activity_watched, MyPasswordChange, TermsOfService, PrivacyPolicy,

)


class TestUrls(TestCase):

    def test_not_exist_url(self):
        with self.assertRaises(Resolver404):
            resolve('/account/notexist')

    def test_profile_edit_url_is_exist(self):
        view = resolve('/account/profile/edit')
        self.assertEqual(view.func.view_class, ProfileEdit)

    def test_profile_image_upload_url_is_exist(self):
        view = resolve('/account/profile/img_upload')
        self.assertEqual(view.func, profile_image_upload)

    def test_user_list_url_is_exist(self):
        view = resolve('/account/list')
        self.assertEqual(view.func.view_class, UserList)

    def test_user_detail_url_is_exist(self):
        view = resolve('/account/1/detail')
        self.assertEqual(view.func.view_class, UserDetail)

    def test_picture_list_url_is_exist(self):
        view = resolve('/account/1/picture_list')
        self.assertEqual(view.func.view_class, UserPictureList)

    def test_follow_url_is_exist(self):
        view = resolve('/account/follow')
        self.assertEqual(view.func, add_or_del_relationship)

    def test_activity_watched_url_is_exist(self):
        view = resolve('/account/activity_watched')
        self.assertEqual(view.func, ajax_activity_watched)

    def test_password_change_url_is_exist(self):
        view = resolve('/account/password/change')
        self.assertEqual(view.func.view_class, MyPasswordChange)