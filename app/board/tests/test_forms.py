from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO

from ..forms import PostCreateForm, PictureForm, PostUpdateForm, CommentForm
from ..models import Post

from PIL import Image

User = get_user_model()


class TestPostCreateForm(TestCase):
    def test_empty_form(self):
        form = PostCreateForm()
        self.assertIn('content', form.fields)

    def test_correct_form(self):
        post = {'content': 'test content'}
        form = PostCreateForm(post)
        self.assertTrue(form.is_valid())

    # def test_too_many_content(self):
    #     post = {'content': 'i' * 2000}
    #     form = PostCreateForm(post)
    #     self.assertFalse(form.is_valid())


class TestPictureCreateForm(TestCase):
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
        print(self.test_img.size)

    def test_empty_form(self):
        form = PictureForm()
        self.assertIn('picture', form.fields)

    def test_correct_form(self):
        data = {
            'picture': self.test_img,
            # 'user': self.user,
            # 'post': self.post,
        }
        form = PictureForm(files=data)
        print(form)
        self.assertTrue(form.is_valid())

    def test_no_data_form(self):
        data = {
            'picture': None,
            # 'user': self.user,
            # 'post': self.post,
        }
        form = PictureForm(files=data)
        print(form)
        self.assertFalse(form.is_valid())


class TestPostUpdateForm(TestCase):

    def test_user_update_form_correct_data(self):
        form = PostUpdateForm(data={'content': 'test update'})
        self.assertTrue(form.is_valid())

    def test_user_update_form_blank_data(self):
        form = PostUpdateForm(data={'content': ''})
        self.assertFalse(form.is_valid())

    def test_user_update_form_no_data(self):
        form = PostUpdateForm(data={})
        self.assertFalse(form.is_valid())


class TestCommentForm(TestCase):

    def test_user_update_form_correct_data(self):
        form = CommentForm(data={'text': 'test update'})
        self.assertTrue(form.is_valid())

    def test_user_update_form_blank_data(self):
        form = CommentForm(data={'text': ''})
        self.assertFalse(form.is_valid())

    def test_user_update_form_no_data(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())