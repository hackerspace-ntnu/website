from django import template

register = template.Library()


@register.inclusion_tag('reservations/templatetags/week.html', takes_context=True)
def week(context, reservations):
    return {'reservations': reservations,
            'perms': context.get('perms', None)}
