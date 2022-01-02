from django.test import TestCase
from django.urls import reverse


class TestTermsOfServiceView(TestCase):

    def test_terms_of_service_get(self):
        response = self.client.get(reverse('terms_of_service'))
        self.assertTemplateUsed(response, 'myProject/terms_of_service.html')
        self.assertEqual(response.status_code, 200)


class TestPrivacyPolicyView(TestCase):

    def test_privacy_policy_get(self):
        response = self.client.get(reverse('privacy_policy'))
        self.assertTemplateUsed(response, 'myProject/privacy_policy.html')
        self.assertEqual(response.status_code, 200)