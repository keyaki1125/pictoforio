from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import MyUser, Activity, Relationship

User = get_user_model()


class UserModelTest(TestCase):

    def test_is_empty(self):
        saved_user = User.objects.all()
        self.assertEqual(saved_user.count(), 0)

    def test_is_count_one(self):
        user = User(email='test@mail.com', password='test1234')
        user.save()
        saved_user = User.objects.all()
        self.assertEqual(saved_user.count(), 1)

    def test_saving_and_retrieving_user(self):
        email = 'test@mail.com'
        password = 'test1234'
        user = User(email=email, password=password)
        user.save()

        saved_user = User.objects.all()
        actual_user = saved_user[0]

        self.assertEqual(actual_user.email, email)
        self.assertEqual(actual_user.password, password)