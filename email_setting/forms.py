from django.forms import ModelForm
from core.models import EmailSettings
from django import forms
from django.utils.safestring import mark_safe


class EmailSettingsForm(ModelForm):
    class Meta:
        model = EmailSettings
        fields = '__all__'
