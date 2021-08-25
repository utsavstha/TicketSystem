from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm
from django.contrib.auth.models import User, Group
from core.models import *
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.decorators import login_required


class UserForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'password1',
                  'password2', 'is_superuser', 'is_admin', 'is_staff']
        labels = {
            "is_superuser": "Admin",
            "is_staff": "Staff",
        }


class UpdateUserForm(UserChangeForm):
    # password = forms.CharField(widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    password = ReadOnlyPasswordHashField(
        label=("Password")
    )

    def __init__(self, instance=None, data=None, initial=None, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields[
            'password'].help_text = f'<a href=\"http://127.0.0.1:8000/change_password/{instance.id}">Change Password</a>'
        self.fields['email'] = forms.CharField(
            widget=forms.TextInput(), initial=instance.email)
        self.fields['first_name'] = forms.CharField(
            widget=forms.TextInput(), initial=instance.first_name)
        self.fields['last_name'] = forms.CharField(
            widget=forms.TextInput(), initial=instance.last_name)

        self.fields['is_superuser'] = forms.BooleanField(
            initial=instance.is_superuser)
        self.fields['is_admin'] = forms.BooleanField(
            initial=instance.is_admin)
        self.fields['is_staff'] = forms.BooleanField(
            initial=instance.is_staff)

    class Meta:
        model = Account

        fields = ['first_name', 'last_name',
                  'email', 'password', 'is_superuser', 'is_admin', 'is_staff']
        # if self.id != None:
        #     self.fields['password'].help_text = '<a href=\"{}\">\"{self.id}\"</a>.'
