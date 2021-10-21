from django.forms import ModelForm
from core.models import *
from django import forms


class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'group', 'supervisor']
    group = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple, required=False
    )

    supervisor = forms.ModelMultipleChoiceField(
        queryset=Account.objects.all(),
        widget=forms.CheckboxSelectMultiple, required=False
    )
