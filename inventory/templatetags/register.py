from django import template
from inventory.forms import ItemForm

register = template.Library()

@register.inclusion_tag("inventory/edit-modal.html")
def edit_item_form(item):
    form = ItemForm(instance=item)
    return {'form': form}
