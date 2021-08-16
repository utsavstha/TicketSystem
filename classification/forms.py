from django.forms import ModelForm
from core.models import Classification
from django import forms
from django.utils.safestring import mark_safe


class ClassificationForm(ModelForm):
    class Meta:
        model = Classification
        fields = '__all__'
