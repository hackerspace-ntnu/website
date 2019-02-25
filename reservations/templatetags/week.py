import calendar

from django import template

register = template.Library()


@register.inclusion_tag('reservations/templatetags/week.html', takes_context=True)
def week(context, reservations):
    return {'reservations': reservations,
            'perms': context.get('perms', None)}


@register.filter(name='nob_day')
def get_norwegian_day_name(day):
    nob_days = ['Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lørdag', 'Søndag']
    translation = dict(zip(calendar.day_name, nob_days))
    return translation.get(day, None)

