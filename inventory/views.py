from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Item, ItemLoan


class InventoryListView(ListView):
    '''Searchable list of items in inventory'''

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
        else:
            # Default to sorting by ID (i.e. newest first)
            items = items.order_by('-id')

        return items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_name'] = self.request.GET.get('filter_name', '')
        context['sort_by'] = self.request.GET.get('sort_by', '')
        return context

class ItemDetailView(DetailView):
    '''Detail view for individual inventory items'''

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
    '''View for creating new inventory items'''

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
    '''View for updating inventory items'''

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
    '''View for deleting inventory items'''

    model = Item
    permission_required = 'inventory.delete_item'
    success_url = reverse_lazy('inventory:inventory')
    success_message = 'Lagerinnslaget er fjernet.'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class ItemLoanListView(ListView, PermissionRequiredMixin):
    '''View for viewing all loan applications'''

    model = ItemLoan
    permission_required = 'inventory.view_itemloan'
    template_name = 'inventory/loan_applications.html'
    context_object_name = 'applications'

    def get_queryset(self):
        application_filter = self.request.GET.get('filter', '')
        name_filter = self.request.GET.get('filter_name', '')

        applications = ItemLoan.objects.all()
        if application_filter == 'overdue':
            # very roundabout way but we need applications to be a queryset
            applications = ItemLoan.objects.filter(id__in=[app for app in applications if app.overdue()])
        elif application_filter == 'not_approved':
            applications = ItemLoan.objects.filter(approver__isnull=True)
        elif application_filter == 'open':
            applications = ItemLoan.objects.filter(returned_date__isnull=True)
        elif application_filter == 'closed':
            applications = ItemLoan.objects.filter(returned_date__isnull=False)
        
        # Additionally filter by the name of the applicant
        if name_filter:
            applications = applications.filter(contact_name__contains=name_filter)

        return applications.order_by('loan_to')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        context['filter_name'] = self.request.GET.get('filter_name', '')
        return context


class ItemLoanDetailView(DetailView, PermissionRequiredMixin):
    '''View for a single loan application'''
    
    model = ItemLoan
    permission_required = 'inventory.view_itemloan'
    template_name = 'inventory/loan_detail.html'
    context_object_name = 'app'


class ItemLoanApproveView(TemplateView, PermissionRequiredMixin, SuccessMessageMixin):
    '''Endpoint for approving loans'''

    permission_required = 'inventory.view_itemloan'
    success_message = 'Lånet er godkjent'

    def get(self, request, pk=None):
        if not pk:
            return HttpResponseRedirect(reverse('inventory:loans'))

        application = get_object_or_404(ItemLoan, id=pk)
        application.loan_from = timezone.now()
        application.approver = request.user
        application.save()

        return HttpResponseRedirect(reverse('inventory:loan_application', kwargs={'pk': pk}))


class ItemLoanReturnedView(TemplateView, PermissionRequiredMixin, SuccessMessageMixin):
    '''Endpoint for marking loans as returned'''

    permission_required = 'inventory.view_itemloan'
    success_message = 'Lånet er markert som levert'

    def get(self, request, pk=None):
        if not pk:
            return HttpResponseRedirect(reverse('inventory:loans'))

        application = get_object_or_404(ItemLoan, id=pk)
        application.returned_date = timezone.now()
        application.save()

        return HttpResponseRedirect(reverse('inventory:loan_application', kwargs={'pk': pk}))
