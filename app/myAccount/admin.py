from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _

from .models import MyUser, Activity


class MyUserChangeForm(UserChangeForm):

    class Meta:
        model = MyUser
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = MyUser
        """passwordはデフォルトで含まれている"""
        fields = ('email',)


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('nickname', 'introduce', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_guest')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'nickname', 'is_active', 'update_at', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'nickname')
    ordering = ('-update_at',)


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Activity)