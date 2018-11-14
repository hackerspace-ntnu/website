from django import template

register = template.Library()


@register.inclusion_tag('reservations/templatetags/week.html')
def week(reservations):
    return {'reservations': reservations}
