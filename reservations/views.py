from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from reservations.forms import QueueForm, ReservationForm
from reservations.helpers import get_queue_timetable
from reservations.models import Queue, Reservation


class QueueDetailView(DetailView):
    model = Queue

    def get_context_data(self, **kwargs):
        context = dict()
        context['reservations'] = get_queue_timetable(queue=self.object, week_delta=kwargs.pop('week', 0))
        context.update(kwargs)
        return super().get_context_data(**context)


class QueueListView(ListView):
    model = Queue
    queryset = Queue.objects.filter(published=True)


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


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    redirect_field_name = 'login/'
    form_class = ReservationForm
    success_url = reverse_lazy('reservations:queue_list')

    def get_form_kwargs(self):
        # get parent queue pk, add to kwargs
        kwargs = super(ReservationCreateView, self).get_form_kwargs()
        kwargs.update(self.kwargs)
        return kwargs

"""
    def get_success_url(self):
        return reverse(
            'reservations:queue_detail',
            kwargs={'pk': get_object_or_404(Reservation, pk=self.kwargs['pk']).parent_queue.pk}
        )
"""


class ReservationDeleteView(UserPassesTestMixin, DeleteView):
    model = Reservation
    redirect_field_name = 'login/'
    success_url = reverse_lazy('reservations:queue_list')

    def test_func(self):
        return self.request.user == get_object_or_404(Reservation, pk=self.kwargs['pk']).user \
               or self.request.user.has_perm('reservations.delete_queue')


class ReservationUpdateView(UserPassesTestMixin, UpdateView):
    model = Reservation
    redirect_field_name = 'login/'
    form_class = ReservationForm

    def get_success_url(self):
        return reverse(
            'reservations:queue_detail',
            kwargs={'pk': get_object_or_404(Reservation, pk=self.kwargs['pk']).parent_queue.pk}
        )

    def test_func(self):
        return self.request.user == get_object_or_404(Reservation, pk=self.kwargs['pk']).user \
               or self.request.user.has_perm('reservations.edit_reservation')




