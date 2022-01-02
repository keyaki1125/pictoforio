from django.test import TestCase
from django.urls import resolve

from ..views import TermsOfService, PrivacyPolicy


class TestUrls(TestCase):
    def test_terms_of_service_url_is_exist(self):
        view = resolve('/terms_of_service')
        self.assertEqual(view.func.view_class, TermsOfService)

    def test_privacy_policy_url_is_exist(self):
        view = resolve('/privacy_policy')
        self.assertEqual(view.func.view_class, PrivacyPolicy)