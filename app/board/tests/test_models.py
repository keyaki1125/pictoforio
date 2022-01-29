from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from ..models import Post, Picture, Comment, Like

from io import BytesIO
import random

from PIL import Image

User = get_user_model()


class PostModelTest(TestCase):

    def setUp(self):
        self.email = 'test@mail.com'
        self.password = 'test5232'
        self.user = User.objects.create_user(email=self.email, password=self.password, is_active=True)

    def test_is_empty(self):
        saved_post = Post.objects.all()
        self.assertEqual(saved_post.count(), 0)

    def test_is_count_one(self):
        post = Post(owner=self.user, content='test', is_publish=True)
        post.save()
        saved_post = Post.objects.all()
        self.assertEqual(saved_post.count(), 1)

    def test_saving_and_retrieving_post(self):
        user = self.user
        content = 'test'
        is_publish = True
        post = Post(owner=user, content=content, is_publish=is_publish)
        post.save()

        saved_post = Post.objects.all()
        actual_post = saved_post[0]

        self.assertEqual(actual_post.owner, user)
        self.assertEqual(actual_post.content, content)
        self.assertEqual(actual_post.is_publish, is_publish)


class PictureModelTest(TestCase):
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

    def test_is_empty(self):
        saved_picture = Picture.objects.all()
        self.assertEqual(saved_picture.count(), 0)

    def test_is_count_one(self):
        picture = Picture(picture=self.test_img, post=self.post, user=self.user)
        picture.save()
        saved_picture = Picture.objects.all()
        self.assertEqual(saved_picture.count(), 1)

    def test_saving_and_retrieving_post(self):
        picture = Picture(picture=self.test_img, post=self.post, user=self.user)
        picture.save()
        saved_picture = Picture.objects.all()
        actual_picture = saved_picture[0]

        self.assertNotEqual(actual_picture.picture, self.test_img)
        self.assertEqual(actual_picture.post, self.post)
        self.assertEqual(actual_picture.user, self.user)

    def test_picture_resize(self):
        picture = Picture(picture=self.test_img, post=self.post, user=self.user)
        picture.save()
        saved_picture = Picture.objects.all()
        actual_picture = saved_picture[0]

        self.assertLessEqual(actual_picture.picture.width, 1000)


class LikeModelTest(TestCase):

    def setUp(self):
        self.email = 'test@mail.com'
        self.password = 'test5232'
        self.user = User.objects.create_user(email=self.email, password=self.password, is_active=True)

        self.content = 'test content'
        self.is_publish = True
        self.post = Post.objects.create(owner=self.user, content=self.content, is_publish=self.is_publish)

    def test_is_empty(self):
        saved_like = Like.objects.all()
        self.assertEqual(saved_like.count(), 0)

    def test_is_count_one(self):
        like = Like(post=self.post, user=self.user)
        like.save()
        saved_like = Like.objects.all()
        self.assertEqual(saved_like.count(), 1)

    def test_saving_and_retrieving_post(self):
        like = Like(post=self.post, user=self.user)
        like.save()
        saved_like = Like.objects.all()
        actual_like = saved_like[0]

        self.assertEqual(actual_like.post, self.post)
        self.assertEqual(actual_like.user, self.user)


class CommentModelTest(TestCase):
    def setUp(self):
        self.email = 'test@mail.com'
        self.password = 'test5232'
        self.user = User.objects.create_user(email=self.email, password=self.password, is_active=True)

        self.content = 'test content'
        self.is_publish = True
        self.post = Post.objects.create(owner=self.user, content=self.content, is_publish=self.is_publish)

    def test_is_empty(self):
        saved_comment = Comment.objects.all()
        self.assertEqual(saved_comment.count(), 0)

    def test_is_count_one(self):
        comment = Comment(text='test comment', post=self.post, user=self.user)
        comment.save()
        saved_comment = Comment.objects.all()
        self.assertEqual(saved_comment.count(), 1)

    def test_saving_and_retrieving_post(self):
        text = 'test comment'
        comment = Comment(text=text, post=self.post, user=self.user)
        comment.save()
        saved_comment = Comment.objects.all()
        actual_comment = saved_comment[0]

        self.assertEqual(actual_comment.text, text)
        self.assertEqual(actual_comment.post, self.post)
        self.assertEqual(actual_comment.user, self.user)