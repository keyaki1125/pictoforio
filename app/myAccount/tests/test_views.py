import base64
from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy

User = get_user_model()


class TestUserListView(TestCase):

    def test_user_list_get(self):
        email = 'test@mail.com'
        password = 'test5232'
        User.objects.create_user(email=email, password=password)
        self.client.login(email=email, password=password)
        response = self.client.get(reverse('myAccount:user_list'))
        self.assertTemplateUsed(response, 'account/user_list.html')
        self.assertEqual(response.status_code, 200)


class TestUserDetailView(TestCase):

    def test_user_detail_get(self):
        email = 'test@mail.com'
        password = 'test5232'
        user = User.objects.create_user(email=email, password=password)
        self.client.login(email=email, password=password)
        response = self.client.get(reverse('myAccount:user_detail', kwargs={'pk': user.pk}))
        self.assertTemplateUsed(response, 'account/base_user_page.html')
        self.assertEqual(response.status_code, 200)


class TestUserPictureListView(TestCase):

    def test_user_picture_list_get(self):
        email = 'test@mail.com'
        password = 'test5232'
        user = User.objects.create_user(email=email, password=password)
        self.client.login(email=email, password=password)
        response = self.client.get(reverse('myAccount:picture_list', kwargs={'pk': user.pk}))
        self.assertTemplateUsed(response, 'account/picture_list.html')
        self.assertEqual(response.status_code, 200)


class TestProfileEditView(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.email = 'test@mail.com'
        cls.password = 'test5232'
        cls.user = User.objects.create_user(email=cls.email, password=cls.password)

    def test_profile_update_get(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('myAccount:edit_profile'))
        self.assertTemplateUsed(response, 'account/edit_profile.html')

    def test_profile_update_post(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('myAccount:edit_profile'),
                                    data={'nickname': 'Mike',
                                          'introduce': 'Hello, everyone'},
                                    follow=True)
        self.assertRedirects(response,
                             reverse('myAccount:user_detail', kwargs={'pk': self.user.pk}),
                             status_code=302)


class TestPasswordChangeView(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.email = 'test@mail.com'
        cls.password = 'test5232'
        cls.user = User.objects.create_user(email=cls.email, password=cls.password)

    def test_password_change_get(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('myAccount:my_password_change'))
        self.assertTemplateUsed(response, 'account/password_change.html')

    def test_password_change_post(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('myAccount:my_password_change'),
                                    data={'oldpassword': 'test5232',
                                          'password1': 'newtest5232',
                                          'password2': 'newtest5232'},
                                    follow=True)
        self.assertRedirects(response,
                             reverse('myAccount:user_detail', kwargs={'pk': self.user.pk}),
                             status_code=302)


# class TestProfileImageUploadView(TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.email = 'test@mail.com'
#         cls.password = 'test5232'
#         cls.user = User.objects.create_user(email=cls.email, password=cls.password)
#
#         # pillow(PIL)を用いてサンプルダミー画像生成
#         img = Image.new('RGBA', size=(1000, 1000), color=(255, 255, 255))
#         img_io = BytesIO()  # a BytesIO object for saving image
#         img.save(img_io, 'png')
#         img_io.name = 'test_img.png'
#         img_io.seek(0)
#         cls.test_img = SimpleUploadedFile(
#             img_io.name,
#             img_io.read(),
#             content_type='image/png')
#
#     def test_profile_image_upload_get(self):
#         pass
#
#     def test_profile_image_upload_post(self):
#         # encoded_img = base64.b64encode(self.test_img)
#         width = 1200
#         height = 400
#         graph = Image.new("RGB", (width, height), (100, 0, 0))  # 画像オブジェクトの生成
#         # draw = ImageDraw.Draw(graph)  # 画像オブジェクトの編集用インスタンスの生成
#
#         # ここでdrawインスタンスを用いてgraph上に文字を書いたりして編集します
#         # わたしは、データベースから読み出したタスク情報の文字列を書いたりしました
#
#         buffer = BytesIO()  # メモリ上への仮保管先を生成
#         graph.save(buffer, format="PNG")  # pillowのImage.saveメソッドで仮保管先へ保存
#
#         # 保存したデータをbase64encodeメソッド読み込み
#         # -> byte型からstr型に変換
#         # -> 余分な区切り文字(　'　)を削除
#         base64_img = base64.b64encode(buffer.getvalue()).decode().replace("'", "")
#
#         self.client.login(email=self.email, password=self.password)
#         response = self.client.post(reverse('myAccount:image_upload'),
#                                     data={'image': base64_img},
#                                     **{'HTTP_X_REQUESTED_WITH':
#                                            'XMLHttpRequest'}
#                                     )
#         self.assertEqual(response.status_code, 200)
#         print(str(response.content, encoding='utf8'))
#         print(self.user.avatar)
#         self.assertJSONEqual(str(response.content, encoding='utf8'),
#                              {'imageURL': self.user.avatar})


class TestRelationship(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.email1 = 'test@mail.com'
        cls.password1 = 'test5232'
        cls.user1 = User.objects.create_user(email=cls.email1, password=cls.password1)

        cls.email2 = 'test2@mail.com'
        cls.password2 = 'test5232'
        cls.user2 = User.objects.create_user(email=cls.email2, password=cls.password2)

    def test_relationship_get(self):
        """@required_get指定があるとHttpResponseNotAllowed(=405)が返される"""
        self.client.login(email=self.email1, password=self.password1)
        response = self.client.get(reverse('myAccount:follow'), follow=True)
        self.assertEqual(response.status_code, 405)

    def test_relationship_post(self):
        self.client.login(email=self.email1, password=self.password1)
        response = self.client.post(reverse('myAccount:follow'),
                                    data={'follow_target_id': self.user2.pk},
                                    **{'HTTP_X_REQUESTED_WITH':
                                           'XMLHttpRequest'}  # バックエンド側でcsrf_tokenが設定されていないので任意に設定する必要がある
                                    )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {'relation': True, 'follow_target_id': self.user2.pk})


class TestAjaxActivityWatched(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.email = 'test@mail.com'
        cls.password = 'test5232'
        cls.user = User.objects.create_user(email=cls.email, password=cls.password)

    def test_ajax_activity_watched_get(self):
        """@required_get指定があるとHttpResponseNotAllowed(=405)が返される"""
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('myAccount:activity_watched'), follow=True)
        self.assertEqual(response.status_code, 405)

    def test_ajax_activity_watched_post(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('myAccount:activity_watched'),
                                    follow=True,
                                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
                                    )
        self.assertEqual(response.status_code, 200)