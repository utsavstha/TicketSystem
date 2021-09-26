import os

from django import template


register = template.Library()

attachment = False

@register.filter
def filename(value):
    return os.path.basename(value.file.name)

@register.simple_tag
def setvar(val=False):
  return val

@register.simple_tag
def changeStatement(status):
    return not status