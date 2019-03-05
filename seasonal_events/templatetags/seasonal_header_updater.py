from django import template
from seasonal_events.models import Season
register = template.Library()


#Date conflicts can arise
@register.simple_tag()
def current_season():
    for s in Season.objects.filter(active=True):
        if s.isNow():
            return "seasonal_events/seasonal_logos/"+s.header_name+".png"
    return "website/img/logo/Hackerspace_huge.png"
