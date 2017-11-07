from django import template

register = template.Library()


@register.inclusion_tag('inventory/cards/tag_checkboxes.html')
def tag_hierarchy(tags, level, padding):
    return {'tags': tags,
            'level': level,
            'next_level': level + 1,
            'padding': padding,
            }
