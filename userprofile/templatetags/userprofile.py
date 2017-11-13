from userprofile.models import Profile
from django import template

register = template.Library()
@register.simple_tag
def get_profile(user_id,attr):
    try:
        return getattr(Profile.objects.get(user__id=user_id), attr)
    except:
        return ''

