from django.shortcuts import render
from django.views.generic import TemplateView
from .utils import get_shift_weekview_rows, get_shift_weekview_columns

class watchlistView(TemplateView):
    template_name = 'watchlist/watchlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["columns"] = get_shift_weekview_columns()
        context["rows"] = get_shift_weekview_rows()
        return context
