from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group
from core.models import *
from django import forms
from django.utils.safestring import mark_safe


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'users', 'supervisor']
    users = forms.ModelMultipleChoiceField(
        queryset=Account.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    supervisor = forms.ModelMultipleChoiceField(
        queryset=Account.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
