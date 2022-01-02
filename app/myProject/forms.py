from django import forms
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string

import datetime


class ContactForm(forms.Form):
    subject = forms.CharField(
        label='',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "お問合せタイトル",
        })
    )
    name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "お名前",
        }),
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "メールアドレス",
        }),
    )
    message = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': "お問い合わせ本文",
        }),
    )

    def send_email(self):
        subject = self.cleaned_data['subject']
        # message = f"{self.cleaned_data['message']}\n\n送信者：{self.cleaned_data['email']}"
        message = self.cleaned_data['message']
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        now = datetime.datetime.now()
        f_now = now.strftime('%Y年%m月%d日  %H:%M:%S')
        from_email = '{name} <{email}>'.format(name=name, email=email)
        recipient_list = [settings.EMAIL_HOST_USER]  # 受信者リスト
        context = {
            'subject': subject,
            'message': message,
            'name': name,
            'email': email,
            'now': f_now
        }
        send_message = render_to_string('myProject/mail.txt', context,)
        try:
            send_mail(subject, send_message, from_email, recipient_list)
        except BadHeaderError:
            return HttpResponse("無効なヘッダが検出されました。")