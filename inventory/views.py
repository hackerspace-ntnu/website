from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Item


class InventoryListView(ListView):
    model = Item
    paginate_by = 15
    template_name = 'inventory/inventory.html'

    context_object_name = 'items'

    def get_queryset(self):
        name_filter = self.request.GET.get('filter_name', '')
        sorting_criteria = self.request.GET.get('sort_by', '')

        items = Item.objects.filter(name__icontains=name_filter)
        if sorting_criteria == 'name':
            items = items.order_by('name')
        elif sorting_criteria == 'stock':
            items = items.order_by('-stock')

        return items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_name'] = self.request.GET.get('filter_name', '')
        context['sort_by'] = self.request.GET.get('sort_by', '')
        return context

class ItemDetailView(DetailView):
    model = Item
    template_name = 'inventory/item_detail.html'

    def get_object(self, *args, **kwargs):
        '''Returns the result of the supercall, but tracks a view on the object'''
        obj = super().get_object(*args, **kwargs)
        if obj is None:
            return obj

        obj.views += 1
        obj.save()
        return obj