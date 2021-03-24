from django.shortcuts import render
from django.views.generic import TemplateView
from .utils import get_shift_weekview_rows, get_shift_weekview_columns
from userprofile.models import Skill, Category

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
