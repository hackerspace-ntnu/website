from django.contrib.auth.forms import AuthenticationForm
from django import template

register = template.Library()

@register.inclusion_tag('authentication/login_modal.html')
def LoginModal():
    return {'login_form': AuthenticationForm() }
