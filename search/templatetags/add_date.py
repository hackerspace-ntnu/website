from django import template

register = template.Library()


@register.filter()
def add_date(text, date):
    return text + date.strftime("%d. %B %Y")
