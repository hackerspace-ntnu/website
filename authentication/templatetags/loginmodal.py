from authentication.forms import LoginForm
from django import template

register = template.Library()

@register.inclusion_tag('login_modal.html')
def LoginModal():
    return {'login_form': LoginForm() }
