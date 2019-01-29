from django import template

register = template.Library()


@register.inclusion_tag('website/header.html')
def seasonal_header_updater():
    currentSeason = "none"
    return {"currentSeason": currentSeason}
