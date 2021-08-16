from django.forms import ModelForm
from core.models import *


class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = '__all__'
