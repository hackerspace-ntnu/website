from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag(takes_context=True)
def green_if_current_shift(context, shift, extra_classes=""):
    if shift.start < context["current_time"].time() and shift.end > context["current_time"].time():
        return format_html("<div id='currentShift' class='{}'>", extra_classes)
    return format_html("<div class='{}'>", extra_classes)