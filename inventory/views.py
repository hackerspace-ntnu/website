from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
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
        elif sorting_criteria == 'stock_dsc':
            items = items.order_by('-stock')
        elif sorting_criteria == 'stock_asc':
            items = items.order_by('stock')
        elif sorting_criteria == 'popularity':
            items = sorted(items, key=lambda item: -item.popularity())

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

class ItemCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Item
    fields = ['name', 'stock', 'description', 'thumbnail']
    template_name = 'inventory/edit_item.html'
    permission_required = 'inventory.add_item'
    success_message = 'Gjenstanden er ført inn i lagersystemet.'

    def get_success_url(self):
        return reverse('inventory:item', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        if form.instance.stock < 0:
            form.errors['stock'] = 'Lagerbeholdningen kan ikke være negativ'
            return self.render_to_response(self.get_context_data(form=form))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

class ItemUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Item
    fields = ['name', 'stock', 'description', 'thumbnail']
    template_name = 'inventory/edit_item.html'
    permission_required = 'inventory.change_item'
    success_message = 'Lagerinnslaget er oppdatert.'

    def get_success_url(self):
        return reverse('inventory:item', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        if form.instance.stock < 0:
            form.errors['stock'] = 'Lagerbeholdningen kan ikke være negativ'
            return self.render_to_response(self.get_context_data(form=form))
        return super().form_valid(form)

class ItemDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Item
    permission_required = 'inventory.delete_item'
    success_url = reverse_lazy('inventory:inventory')
    success_message = 'Lagerinnslaget er fjernet.'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)