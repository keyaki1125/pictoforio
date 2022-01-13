from django import forms
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

from .models import Post, Comment, Picture


class PostCreateForm(forms.ModelForm):
    content = forms.CharField(label='本文',
                              max_length=1000,
                              widget=forms.Textarea(attrs={'rows': 5,
                                                           'placeholder': '本文を入力...'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Post
        fields = ('content',)


class PictureForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
        label='ファイル選択...',
    )

    class Meta:
        model = Picture
        exclude = ['user', 'post']


class BasePictureFormSet(forms.BaseInlineFormSet):
    at_least_on_form_required_error = u"画像を最低１つは選択してください"

    def clean(self):
        if not getattr(self.forms[0], "cleaned_data"):
            raise forms.ValidationError(self.at_least_on_form_required_error)


PictureFormset = forms.inlineformset_factory(
    parent_model=Post,
    model=Picture,
    form=PictureForm,
    formset=BasePictureFormSet,
    # exclude=('user',),
    # fields='__all__',
    extra=4,
    max_num=5,
    min_num=1,
    validate_max=True,
    validate_min=True,
    # error_messages={'missing_management_form': 'テスト'},
    error_messages={'too_few_forms': '画像を一つ以上選択してください'},
    # can_delete=False,
)


class MultiplePictureCreateForm(forms.Form):
    picture = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), )

    def clean_picture(self):
        """
        self.cleaned_data['picture']だと最後の一枚しか取得できない。
        ユーザーがアップロードしたファイルはrequest.FILESに格納され、フォームにはfiles=request.FILESとして渡される。
        フォーム側からはself.filesとしてファイルを扱えるようになっている。
        なので複数画像の場合、self.files.getlist('picture')とする。
        """
        # picture = self.cleaned_data['picture']
        multiple_picture = self.files.getlist('picture')
        if not multiple_picture:
            raise forms.ValidationError('画像を選択してください')

        if len(multiple_picture) > 5:
            raise forms.ValidationError('画像の投稿は5枚までです')

    # def save(self):
    #     """
    #     複数画像を個別に保存し、各ファイルをリストにして返却。
    #     ユーザーがアップロードしたファイルはrequest.FILESに格納され、フォームにはfiles=request.FILESとして渡される。
    #     フォーム側からはself.filesとしてファイルを扱えるようになっている。
    #     """
    #     url_list = []
    #     for picture in self.files.getlist('picture'):
    #         picture_name = default_storage.save(picture.name, picture)
    #         picture_path = default_storage.url(picture_name)
    #         url_list.append(picture_path)
    #     return url_list


# class PostImageCreateForm(forms.ModelForm):
#     class Meta:
#         model = Post


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)
        widgets = {'content': forms.Textarea(attrs={
            'rows': 5,
            'cols': 30,
        })}


class CommentForm(forms.ModelForm):
    # content = forms.CharField(max_length=500,
    #                           widget=forms.Textarea(attrs={'placeholder': 'コメントする...'}))

    class Meta:
        model = Comment
        fields = ('text',)
        # widgets = {'text': forms.TextInput()}


class CommentDeleteForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ()