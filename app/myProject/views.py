from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import ContactForm


class AboutSite(TemplateView):
    template_name = 'myProject/about_site.html'


class TermsOfService(TemplateView):
    """利用規約ページ"""
    template_name = 'myProject/terms_of_service.html'



class PrivacyPolicy(TemplateView):
    """プライバシーポリシーページ"""
    template_name = 'myProject/privacy_policy.html'


class ContactFormView(SuccessMessageMixin, FormView):
    template_name = 'myProject/contact_form.html'
    form_class = ContactForm
    success_message = 'お問い合わせは正常に送信されました'
    success_url = reverse_lazy('board:home')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class ContactResultView(TemplateView):
    template_name = 'myProject/contact_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success'] = "お問い合わせは正常に送信されました。"
        return context