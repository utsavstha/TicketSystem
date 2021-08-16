from django.forms import ModelForm
from core.models import Priority
from django import forms
from django.utils.safestring import mark_safe


class PriorityForm(ModelForm):
    class Meta:
        model = Priority
        fields = '__all__'
