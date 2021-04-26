from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import TemplateView
from .utils import get_shift_weekview_rows, get_shift_weekview_columns
from django.views.generic import View
from django.contrib.auth.mixins import PermissionRequiredMixin
from userprofile.models import Skill, Category
from .models import ShiftSlot
from django.urls import reverse, reverse_lazy

class watchlistView(TemplateView):
    template_name = 'watchlist/watchlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["columns"] = get_shift_weekview_columns()
        context["rows"] = get_shift_weekview_rows()

        skills = Skill.objects.all()
        skill_cats = []
        for skill in skills:
            for cat in skill.categories.all():
                if cat not in skill_cats:
                    skill_cats.append(cat)
        context["skill_categories"] = skill_cats
        return context

class WatchListRegisterView(PermissionRequiredMixin, View):
    """Endpoint for registering for shifts"""

    permission_required = 'watchlist.view_shiftslot'
    success_message = 'Vaktregistreringen er lagret 😃'
    success_url = reverse_lazy('watchlist:vaktliste')

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.success_url

    def get(self, request, *args, **kwargs):
        if 'pk' not in kwargs:
            return HttpResponseRedirect(reverse('watchlist:vaktliste'))

        shift = ShiftSlot.objects.get(id=kwargs['pk'])
        if request.user in shift.watchers.all():
            return HttpResponseRedirect(reverse('watchlist:vaktliste'))
        shift.watchers.add(request.user)
        shift.save()

        return HttpResponseRedirect(self.get_success_url())

class WatchListUnregisterView(PermissionRequiredMixin, View):
    """Endpoint for unregistering from a shift"""

    permission_required = 'watchlist.view_shiftslot'
    success_message = 'Du har blitt avregistrert fra vakten 🥺'
    success_url = reverse_lazy('watchlist:vaktliste')

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.success_url

    def get(self, request, *args, **kwargs):
        if 'pk' not in kwargs:
            return HttpResponseRedirect(reverse('watchlist:vaktliste'))

        shift = ShiftSlot.objects.get(id=kwargs['pk'])
        if request.user not in shift.watchers.all():
            return HttpResponseRedirect(reverse('watchlist:vaktliste'))
        shift.watchers.remove(request.user)
        shift.save()

        return HttpResponseRedirect(self.get_success_url())

class WatchListResetView(PermissionRequiredMixin, View):
    """Endpoint for unregistering everyone from every shift"""

    permission_required = 'watchlist.delete_shiftslot'
    success_message = 'Alle vakter er frigjort'
    success_url = reverse_lazy('watchlist:vaktliste')

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.success_url

    def get(self, request, *args, **kwargs):
        for shift in ShiftSlot.objects.all():
            for user in shift.watchers.all():
                shift.watchers.remove(user)
            shift.save()
        return HttpResponseRedirect(self.get_success_url())
