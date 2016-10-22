from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
from .models import Tag, Item, Loan


def index(request):
    items = Item.objects.all()
    # items.sort(key=lambda a: a.tags.get(pk=1))
    item_dict = {}
    for item in items:
        for tag in item.tags.all():
            try:
                item_dict[tag].append(item)
            except KeyError:
                item_dict[tag] = [item]
    """
    """
    for value in item_dict.values():
        value.sort(key=lambda e: e.name.title())


    dic = {"småelektronikk": ["ledning", "arduino", "motstand"], "brikker": ["arduino", "getcko", "raspberry pi"]}
    context = {
        'items': items,
        'test': item_dict,
    }
    return render(request, 'inventory/index.html', context)


def detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    context = {
        'item': Item.objects.get(pk=item_id)
    }
    return render(request, 'inventory/detail.html', context)

