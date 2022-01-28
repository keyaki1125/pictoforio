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


class RelationshipModelTest(TestCase):
    def setUp(self):
        self.email1 = 'test1@mail.com'
        self.password1 = 'test5232'
        self.user1 = User.objects.create_user(email=self.email1, password=self.password1, is_active=True)

        self.email2 = 'test2@mail.com'
        self.password2 = 'test5232'
        self.user2 = User.objects.create_user(email=self.email2, password=self.password2, is_active=True)

    def test_is_empty(self):
        saved_relationship = Relationship.objects.all()
        self.assertEqual(saved_relationship.count(), 0)

    def test_is_count_one(self):
        Relationship.objects.create(following=self.user1, followed=self.user2)
        saved_relationship = Relationship.objects.all()
        self.assertEqual(saved_relationship.count(), 1)

    def test_saving_and_retrieving_relationship(self):
        Relationship.objects.create(following=self.user1, followed=self.user2)
        saved_relationship = Relationship.objects.all()
        actual_relationship = saved_relationship[0]
        self.assertEqual(actual_relationship.following, self.user1)
        self.assertEqual(actual_relationship.followed, self.user2)


class ActivityModelTest(TestCase):
    def setUp(self):
        self.email1 = 'test1@mail.com'
        self.password1 = 'test5232'
        self.user1 = User.objects.create_user(email=self.email1, password=self.password1, is_active=True)

        self.email2 = 'test2@mail.com'
        self.password2 = 'test5232'
        self.user2 = User.objects.create_user(email=self.email2, password=self.password2, is_active=True)

    def test_is_empty(self):
        saved_activity = Activity.objects.all()
        self.assertEqual(saved_activity.count(), 0)

    def test_is_signal_working(self):
        Relationship.objects.create(following=self.user1, followed=self.user2)
        relationship = Relationship.objects.first()
        saved_activity = Activity.objects.all()
        actual_activity = saved_activity[0]
        self.assertEqual(actual_activity.user, self.user2)
        self.assertEqual(actual_activity.action_user, self.user1)
        self.assertEqual(actual_activity.activity, 30)
        self.assertEqual(actual_activity.model_key, relationship.pk)