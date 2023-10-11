from typing import List

from inventory.models.item import Item


# @atomic
def run_script(list_items: List[dict]):
    items: List[Item] = []
    print(items)
    for item in list_items:
        item = Item(name=item["name"], stock=item["stock"])
        Item.objects.update_or_create(
            name=item["name"], defaults={"stock": item["stock"]}
        )
