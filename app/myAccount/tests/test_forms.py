from django.contrib.auth import get_user_model
from django.test import TestCase

from ..forms import ProfileForm

User = get_user_model()


class TestProfileForm(TestCase):

    def setUp(self):
        self.email = 'test@mail.com'
        self.password = 'test5232'
        User.objects.create_user(email=self.email, password=self.password, is_active=True)

    def test_profile_update_correct_data(self):
        form = ProfileForm(data={'nickname': 'testnickname',
                                 'introduce': 'My name is Test'})
        self.assertTrue(form.is_valid())

    def test_user_update_form_blank_data(self):
        form = ProfileForm(data={'nickname': '', 'introduce': ''})
        self.assertTrue(form.is_valid())

    def test_user_update_form_no_data(self):
        form = ProfileForm(data={})
        self.assertTrue(form.is_valid())