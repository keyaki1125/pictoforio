from django.test import TestCase

from ..forms import ContactForm


class TestContactForm(TestCase):
    def test_empty_form(self):
        form = ContactForm()
        self.assertIn('subject', form.fields)
        self.assertIn('name', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('message', form.fields)

    def test_correct_form(self):
        data = {'subject': 'test-subject',
                'name': 'taro',
                'email': 'test@mail.com',
                'message': 'test-content'}
        form = ContactForm(data)
        self.assertTrue(form.is_valid())