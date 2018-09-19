from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from reservations.forms import QueueForm
from reservations.models import Queue


class QueueDetailView(DetailView):
    model = Queue

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['has_update_permission'] = self.request.user.has_perm('reservations.edit_queue')
        return context


class QueueListView(ListView):
    model = Queue


class QueueCreateView(PermissionRequiredMixin, CreateView):
    model = Queue
    redirect_field_name = '/'
    permission_required = 'reservations.add_queue'
    form_class = QueueForm
    success_url = reverse_lazy('reservations:queue_list')


class QueueUpdateView(PermissionRequiredMixin, UpdateView):
    model = Queue
    form_class = QueueForm
    permission_required = 'reservations.edit_queue'
    success_url = reverse_lazy('reservations:queue_list')
    redirect_field_name = '/'


class QueueDeleteView(PermissionRequiredMixin, DeleteView):
    model = Queue
    redirect_field_name = '/'
    permission_required = 'reservations.delete_queue'
    success_url = reverse_lazy('reservations:queue_list')

