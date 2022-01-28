from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..forms import ProfileForm

User = get_user_model()


class TestProfileForm(TestCase):

    def setUp(self):
        self.email = 'test@mail.com'
        self.password = 'test5232'
        User.objects.create_user(email=self.email, password=self.password, is_active=True)
        # self.guest_email = 'test@mail.com'
        # self.guest_password = 'test5232'
        # User.objects.create_user(email=self.guest_email, password=self.guest_password, is_active=True, is_guest=True)

    def test_profile_update_correct_data(self):
        self.client.login(email=self.email, password=self.password)
        user = User.objects.get(email=self.email)
        request = self.client.get(reverse('myAccount:edit_profile'))
        request.user = user
        form = ProfileForm(data={'nickname': 'testnickname',
                                 'introduce': 'My name is Test'},
                           request=request)
        self.assertTrue(form.is_valid())

    def test_user_update_form_blank_data(self):
        self.client.login(email=self.email, password=self.password)
        user = User.objects.get(email=self.email)
        request = self.client.get(reverse('myAccount:edit_profile'))
        request.user = user
        form = ProfileForm(data={'nickname': '', 'introduce': ''}, request=request)
        self.assertTrue(form.is_valid())

    def test_user_update_form_no_data(self):
        self.client.login(email=self.email, password=self.password)
        user = User.objects.get(email=self.email)
        request = self.client.get(reverse('myAccount:edit_profile'))
        request.user = user
        form = ProfileForm(data={}, request=request)
        self.assertTrue(form.is_valid())