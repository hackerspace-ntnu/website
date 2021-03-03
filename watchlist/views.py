from django.shortcuts import render
from django.views.generic import TemplateView


class watchlistView(TemplateView):
    template_name = 'watchlist/watchlist.html'
