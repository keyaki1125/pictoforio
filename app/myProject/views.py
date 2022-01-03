from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import ContactForm
from board.models import Picture


class Home(LoginRequiredMixin, generic.ListView):
    """ホーム画面は全pictureをランダムに敷き詰めたデザイン"""
    model = Picture
    template_name = 'myProject/home.html'
    ordering = '?'  # order_byの引数を'?'とするとランダムな順番のレコードを取得できる

    def get_queryset(self):
        # application_logger.debug('queryset取得')
        queryset = Picture.objects.filter(post__is_publish=True).order_by('?')
        return queryset


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
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class ContactResultView(TemplateView):
    template_name = 'myProject/contact_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success'] = "お問い合わせは正常に送信されました。"
        return context