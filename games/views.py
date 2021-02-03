from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class SlingerView(TemplateView):
    template_name = 'games/slinger/game.html'