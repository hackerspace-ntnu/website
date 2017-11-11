from django import template
from inventory.models import Tag

register = template.Library()


@register.filter
def get_tags(item):
    return [tag.id for tag in item.tags.all()]


@register.filter
def get_items(tag):
    return [item.id for item in tag.item_set.all()]


@register.filter
def get_tag_children(tag):
    return [t.id for t in tag.children_tags.all()]


@register.filter
def range(number):
    """ For å kjøre en forloop et gitt antall ganger: {% for i in 3|range %} """
    return 'i' * number


@register.simple_tag
def cut_text(word, number):
    # number is the number of characters to show.
    if len(word) <= number:
        return word
    else:
        return word[:number - 3] + '...'
