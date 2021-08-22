from django.forms import ModelForm
from core.models import Priority
from django import forms
from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe


class PriorityForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PriorityForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields["color"].widget = TextInput(
                attrs={"type": "color", "title": self.instance.color}
            )

    class Meta:
        model = Priority
        fields = '__all__'
        widgets = {
            "color": TextInput(attrs={"type": "color"}),
        }
