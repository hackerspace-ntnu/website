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
