from allauth.account.forms import ResetPasswordForm
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class ProfileForm(forms.ModelForm):
    nickname = forms.CharField(label='ニックネーム',
                               max_length=50,
                               widget=forms.TextInput(attrs={'placeholder': '50文字以内で入力...'}))
    introduce = forms.CharField(label='自己紹介',
                                max_length=1024,
                                widget=forms.Textarea(attrs={'rows': 5,
                                                             'placeholder': '自己紹介文を入力...'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        user = self.request.user
        if user.is_guest:
            raise ValidationError('ゲストユーザーは登録情報の編集が制限されます。')

    # def clean_nickname(self):
    #     user = self.request.user
    #
    #     if user.is_guest:
    #         raise ValidationError('ゲストユーザーは登録情報の編集が制限されます。')
    #
    # def clean_introduce(self):
    #     user = self.request.user
    #
    #     if user.is_guest:
    #         raise ValidationError('ゲストユーザーは登録情報の編集が制限されます。')

    class Meta:
        model = User
        fields = ('nickname', 'introduce',)


class MyResetPasswordForm(ResetPasswordForm):
    def clean_email(self):
        super().clean_email()
        if self.cleaned_data['email'] == settings.GUEST_USER_EMAIL:
            raise forms.ValidationError('ゲストユーザーはパスワードをリセットできません')
        return self.cleaned_data['email']