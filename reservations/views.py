from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from reservations.forms import QueueForm, ReservationForm
from reservations.helpers import get_queue_reservations_for_week
from reservations.models import Queue, Reservation


class QueueDetailView(UserPassesTestMixin, DetailView):
    model = Queue

    def get_context_data(self, **kwargs):
        context = dict()
        context['reservations'] = get_queue_reservations_for_week(
            queue=self.object,
            week_delta=kwargs.pop('week', 0)
        )
        context.update(kwargs)
        return super().get_context_data(**context)

    def test_func(self):
        return self.get_object().published or self.request.user.has_perm("reservations.add_queue")


class QueueListView(ListView):
    model = Queue
    queryset = Queue.objects.filter(published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QueueListView, self).get_context_data()
        if self.request.user.has_perm("reservations.add_queue"):
            context["unpublished_queues"] = Queue.objects.filter(published=False)
        return context


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

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        reservation = form.save(commit=False)
        reservation.user = self.request.user
        reservation.parent_queue = form.parent_queue
        reservation.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        # get parent_queue pk and pass on to form
        kwargs = super().get_form_kwargs()
        kwargs['pk'] = self.kwargs['pk']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ReservationCreateView, self).get_context_data(**kwargs)
        context['reservations'] = get_queue_reservations_for_week(
            queue=get_object_or_404(Queue, pk=self.get_form_kwargs()["pk"]),
            week_delta=kwargs.pop('week', 0)
        )
        return context


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




