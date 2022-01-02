from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from ..models import Post, Comment, Picture

User = get_user_model()


class TestHomeView(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.email = 'test@mail.com'
        cls.password = 'test5232'
        cls.user = User.objects.create_user(email=cls.email, password=cls.password)

    def test_home_get(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('board:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'board/home.html')


class TestPostPictureCreateView(TestCase):
    def setUp(self):
        self.email = 'test@mail.com'
        self.password = 'test5232'
        self.user = User.objects.create_user(email=self.email, password=self.password, is_active=True)

        self.content = 'test content'
        self.is_publish = True
        self.post = Post.objects.create(owner=self.user, content=self.content, is_publish=self.is_publish)

        # pillow(PIL)を用いてサンプルダミー画像生成
        img = Image.new('RGBA', size=(1000, 1000), color=(255, 255, 255))
        img_io = BytesIO()  # a BytesIO object for saving image
        img.save(img_io, 'png')
        img_io.name = 'test_img.png'
        img_io.seek(0)
        self.test_img = SimpleUploadedFile(
            img_io.name,
            img_io.read(),
            content_type='image/png')

    def test_post_picture_create_get(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('board:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'board/post_create.html')

    def test_post_picture_create_post(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('board:create'),
                                    data={'content': 'test content',
                                          'picture_set-0-picture': self.test_img,
                                          'picture_set-TOTAL_FORMS': 1,
                                          'picture_set-INITIAL_FORMS': 0,
                                          'picture_set-MIN_NUM_FORMS': 1,
                                          'picture_set-MAX_NUM_FORMS': 5,
                                          },
                                    follow=True)
        print(str(response.content, encoding='utf8'))
        self.assertRedirects(response, reverse('board:post_list'), status_code=302)


class TestPostListView(TestCase):
    def setUp(self):
        self.email = 'test@mail.com'
        self.password = 'test5232'
        self.user = User.objects.create_user(email=self.email, password=self.password, is_active=True)

    def test_post_list_get(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('board:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'board/home_post_list.html')


class TestPrivatePostListView(TestCase):
    def setUp(self):
        self.email = 'test@mail.com'
        self.password = 'test5232'
        self.user = User.objects.create_user(email=self.email, password=self.password, is_active=True)

    def test_private_post_list_get(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('board:private_post_list', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'board/private_post.html')


class TestLikePostListView(TestCase):
    def setUp(self):
        self.email = 'test@mail.com'
        self.password = 'test5232'
        self.user = User.objects.create_user(email=self.email, password=self.password, is_active=True)

    def test_like_post_list_get(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('board:like_post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'board/like_post_list.html')


class TestPostDetailCommentView(TestCase):
    def setUp(self):
        self.email1 = 'test1@mail.com'
        self.password1 = 'test5232'
        self.user1 = User.objects.create_user(email=self.email1, password=self.password1, is_active=True)
        self.email2 = 'test2@mail.com'
        self.password2 = 'test5232'
        self.user2 = User.objects.create_user(email=self.email2, password=self.password2, is_active=True)
        content = 'test content'
        self.post1 = Post.objects.create(content=content, owner=self.user1, is_publish=True)
        self.private_post1 = Post.objects.create(content=content, owner=self.user1, is_publish=False)

    def test_post_detail_get_owner(self):
        self.client.login(email=self.email1, password=self.password1)
        response = self.client.get(reverse('board:post_detail', kwargs={'pk': self.post1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'board/post_detail.html')

    def test_private_post_detail_get_owner(self):
        self.client.login(email=self.email1, password=self.password1)
        response = self.client.get(reverse('board:post_detail', kwargs={'pk': self.private_post1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'board/post_detail.html')

    def test_private_post_detail_get_other(self):
        self.client.login(email=self.email2, password=self.password2)
        response = self.client.get(reverse('board:post_detail', kwargs={'pk': self.private_post1.pk}))
        print(response.status_code)
        self.assertEqual(response.status_code, 403)


class TestPostUpdateView(TestCase):
    def setUp(self):
        self.email = 'test@mail.com'
        self.password = 'test5232'
        self.user = User.objects.create_user(email=self.email, password=self.password, is_active=True)

        self.content = 'test content'
        self.is_publish = True
        self.post = Post.objects.create(owner=self.user, content=self.content, is_publish=self.is_publish)

        # pillow(PIL)を用いてサンプルダミー画像生成
        img1 = Image.new('RGBA', size=(1000, 1000), color=(255, 255, 255))
        img2 = Image.new('RGBA', size=(1000, 1000), color=(255, 255, 255))
        img_io1 = BytesIO()  # a BytesIO object for saving image
        img_io2 = BytesIO()  # a BytesIO object for saving image
        img1.save(img_io1, 'png')
        img2.save(img_io2, 'png')
        img_io1.name = 'test_img_1.png'
        img_io2.name = 'test_img_2.png'
        img_io1.seek(0)
        img_io2.seek(0)
        self.test_img_1 = SimpleUploadedFile(
            img_io1.name,
            img_io1.read(),
            content_type='image/png')
        self.test_img_2 = SimpleUploadedFile(
            img_io2.name,
            img_io2.read(),
            content_type='image/png')
        self.picture = Picture.objects.create(user=self.user, post=self.post, picture=self.test_img_1)

    def test_post_update_get(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('board:post_update', kwargs={'pk': self.post.pk}))
        # print(vars(response))
        # self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'board/post_update.html')

    def test_post_update_post(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(reverse('board:post_update', kwargs={'pk': self.post.pk}),
                                    data={'content': 'test content',
                                          'picture_set-0-picture': self.test_img_2,
                                          'picture_set-TOTAL_FORMS': 5,
                                          'picture_set-INITIAL_FORMS': 0,
                                          'picture_set-MIN_NUM_FORMS': 1,
                                          'picture_set-MAX_NUM_FORMS': 5,
                                          },
                                    follow=True)
        self.assertRedirects(response, reverse('board:post_detail', kwargs={'pk': self.post.pk}), status_code=302)


class TestPostDeleteView(TestCase):
    def setUp(self):
        self.email1 = 'test1@mail.com'
        self.password1 = 'test5232'
        self.user1 = User.objects.create_user(email=self.email1, password=self.password1, is_active=True)
        self.email2 = 'test2@mail.com'
        self.password2 = 'test5232'
        self.user2 = User.objects.create_user(email=self.email2, password=self.password2, is_active=True)
        content = 'test content'
        self.post1 = Post.objects.create(content=content, owner=self.user1, is_publish=True)
        self.private_post1 = Post.objects.create(content=content, owner=self.user1, is_publish=False)

    def test_post_delete_get(self):
        self.client.login(email=self.email1, password=self.password1)
        response = self.client.get(reverse('board:post_delete', kwargs={'pk': self.post1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'board/post_delete.html')

    def test_post_delete_post(self):
        self.client.login(email=self.email1, password=self.password1)
        response = self.client.post(reverse('board:post_delete', kwargs={'pk': self.post1.pk}))
        print(vars(response))
        self.assertRedirects(response,
                             reverse('myAccount:user_detail', kwargs={'pk': self.user1.pk}),
                             status_code=302)

    def test_post_delete_get_other(self):
        self.client.login(email=self.email2, password=self.password2)
        response = self.client.get(reverse('board:post_delete', kwargs={'pk': self.private_post1.pk}))
        self.assertEqual(response.status_code, 403)

    def test_post_delete_post_other(self):
        self.client.login(email=self.email2, password=self.password2)
        response = self.client.post(reverse('board:post_delete', kwargs={'pk': self.private_post1.pk}))
        self.assertEqual(response.status_code, 403)


class TestAjaxLikeView(TestCase):
    def setUp(self):
        self.email1 = 'test1@mail.com'
        self.password1 = 'test5232'
        self.user1 = User.objects.create_user(email=self.email1, password=self.password1, is_active=True)
        self.email2 = 'test2@mail.com'
        self.password2 = 'test5232'
        self.user2 = User.objects.create_user(email=self.email2, password=self.password2, is_active=True)
        content = 'test content'
        self.post1 = Post.objects.create(content=content, owner=self.user1, is_publish=True)

    def test_ajax_like_get(self):
        """@required_get指定があるとHttpResponseNotAllowed(=405)が返される"""
        self.client.login(email=self.email1, password=self.password1)
        response = self.client.get(reverse('board:like'), follow=True)
        self.assertEqual(response.status_code, 405)

    def test_ajax_like_post(self):
        self.client.login(email=self.email1, password=self.password1)
        response = self.client.post(reverse('board:like'),
                                    data={'post_id': self.post1.pk},
                                    follow=True,
                                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
                                    )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {'post_id': self.post1.pk, 'liked': True, 'like_count': self.post1.like_set.count()})


class TestAjaxCommentView(TestCase):
    def setUp(self):
        self.email1 = 'test1@mail.com'
        self.password1 = 'test5232'
        self.user1 = User.objects.create_user(email=self.email1, password=self.password1, is_active=True)
        self.email2 = 'test2@mail.com'
        self.password2 = 'test5232'
        self.user2 = User.objects.create_user(email=self.email2, password=self.password2, is_active=True)
        content = 'test content'
        self.post1 = Post.objects.create(content=content, owner=self.user1, is_publish=True)

    def test_ajax_comment_get(self):
        """@required_get指定があるとHttpResponseNotAllowed(=405)が返される"""
        self.client.login(email=self.email1, password=self.password1)
        response = self.client.get(reverse('board:comment'), follow=True)
        self.assertEqual(response.status_code, 405)

    def test_ajax_like_post(self):
        self.client.login(email=self.email1, password=self.password1)
        response = self.client.post(reverse('board:comment'),
                                    data={'post_id': self.post1.pk,
                                          'text': 'test comment'},
                                    follow=True,
                                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
                                    )
        # print(str(response.content, encoding='utf8'))
        self.assertEqual(response.status_code, 200)
        # self.assertJSONEqual(str(response.content, encoding='utf8'),
        #                      {'post_id': self.post1.pk, 'liked': True, 'like_count': self.post1.like_set.count()})


class TestAjaxCommentDeleteView(TestCase):
    def setUp(self):
        self.email1 = 'test1@mail.com'
        self.password1 = 'test5232'
        self.user1 = User.objects.create_user(email=self.email1, password=self.password1, is_active=True)
        self.email2 = 'test2@mail.com'
        self.password2 = 'test5232'
        self.user2 = User.objects.create_user(email=self.email2, password=self.password2, is_active=True)
        content = 'test content'
        self.post1 = Post.objects.create(content=content, owner=self.user1, is_publish=True)
        text = 'test comment'
        self.comment = Comment.objects.create(text=text, user=self.user1, post=self.post1)

    def test_ajax_comment_get(self):
        """@required_get指定があるとHttpResponseNotAllowed(=405)が返される"""
        self.client.login(email=self.email1, password=self.password1)
        response = self.client.get(reverse('board:comment'), follow=True)
        self.assertEqual(response.status_code, 405)

    def test_ajax_comment_post(self):
        self.client.login(email=self.email1, password=self.password1)
        response = self.client.post(reverse('board:comment'),
                                    data={'post_id': self.post1.pk,
                                          'comment_id': self.comment.pk},
                                    follow=True,
                                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
                                    )
        # print(str(response.content, encoding='utf8'))
        self.assertEqual(response.status_code, 200)