from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class TimeTableView(TemplateView):
    template_name = "internal/timetable.html"
