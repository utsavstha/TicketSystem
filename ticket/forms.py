from django.forms import ModelForm
from django.contrib.auth.models import User, Group
from core.models import *
from django import forms
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.conf import settings
from django.urls import reverse
from priority import views
from django.forms import ClearableFileInput

from django.contrib.admin.widgets import FilteredSelectMultiple

# class RelatedFieldWidgetCanAdd(widgets.Select):

#     def __init__(self, related_model, related_url=None, *args, **kw):

#         super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)

#         if not related_url:
#             rel_to = related_model
#             info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
#             related_url = 'admin:%s_%s_add' % info

#         # Be careful that here "reverse" is not allowed
#         self.related_url = related_url

#     def render(self, name, value, *args, **kwargs):
#         self.related_url = reverse(views.create_priority)
#         output = [super(RelatedFieldWidgetCanAdd, self).render(
#             name, value, *args, **kwargs)]
#         output.append('<a href="%s" class="add-another" style="margin-top: 40px;"id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' %
#                       (self.related_url, name))
#         output.append('<img src="%s/images/add.png" width="20" height="20" style="margin-top: 10px;" alt="%s"/></a>' %
#                       (settings.STATIC_URL, 'Add Another'))
#         return mark_safe(''.join(output))


# class TicketForm(ModelForm):
#     description = forms.CharField(widget=forms.Textarea)

#     class Meta:
#         model = Ticket
#         fields = ['title', 'priority', 'classification',
#                   'assigned_group', 'board', 'assigned_user', 'can_staff_complete', 'description']
#         widgets = {
#             'assigned_group': FilteredSelectMultiple('assigned_group', False),
#             'board': FilteredSelectMultiple('board', False),
#             'assigned_user': FilteredSelectMultiple('assigned_user', False)

#         }


class TicketAttachmentForm(forms.ModelForm):

    class Meta:
        model = TicketAttachment
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }
