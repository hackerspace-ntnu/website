from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Item


class InventoryView(ListView):
    model = Item
    paginate_by = 3
    template_name = 'inventory/inventory.html'

    context_object_name = 'items'

    def get_queryset(self):
        return Item.objects.all()


class ItemDetailView(DetailView):
    model = Item
    template_name = 'inventory/item_detail.html'