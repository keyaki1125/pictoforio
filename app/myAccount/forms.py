from django import forms
from django.contrib.auth import get_user_model

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
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('nickname', 'introduce',)