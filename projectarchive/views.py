from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from datetime import datetime, timedelta
from .forms import ArticleForm
from .models import Projectarticle
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


# class ArticleListView(ListView):
class ArticleListView(ListView):
    Model = Projectarticle
    template_name = "projectarchive/projectarchive.html"
    paginate_by = 10

    def get_queryset(self):
        # Retrieve published articles (so no drafts)
        articles = Projectarticle.objects.order_by('-pub_date').filter(draft=False)

        # Decide if visitor should see internal articles
        if self.request.user.has_perm("projectarchive.can_view_internal_article"):
            return articles
        else:
            return articles.filter(internal=False)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # Retrieve any user drafts if logged in
        if self.request.user.has_perm("projectarchive.add_article"):
            context['drafts'] = Projectarticle.objects.order_by('-pub_date').filter(author=self.request.user,draft=True)

        return context


class ArticleView(DetailView):
    model = Projectarticle
    template_name = "projectarchive/article.html"

    def dispatch(self, request, *args, **kwargs):

        article = self.get_object()

        # If the article is internal, check if user has the permission to view.
        if self.get_object().internal and not request.user.has_perm("projectarchive.can_view_internal_article"):

            # Stores log-in prompt message to be displayed with redirect request
            messages.add_message(request, messages.WARNING, 'Logg inn for å se intern artikkel')

            return redirect("/")

        # If the article is a draft, check if user is the author
        if article.draft and not request.user == article.author:

            # Stores log-in prompt message to be displayed with redirect request
            messages.add_message(request, messages.WARNING, 'Du har ikke tilgang til artikkelen')

            return redirect("/")

        return super(ArticleView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        return context



class ArticleCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Projectarticle
    form_class = ArticleForm
    template_name = "projectarchive/edit_article.html"
    permission_required = "projectarchive.add_article"

    def get_success_message(self, cleaned_data):
        if self.object.draft:
            return "Artikkelen er opprettet som utkast"
        return "Artikkelen er opprettet og publisert"

    def get_success_url(self):
        return reverse('projectarchive:details', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Projectarticle
    form_class = ArticleForm
    template_name = "projectarchive/edit_article.html"
    permission_required = "projectarchive.change_article"
    success_message = "Artikkelen er oppdatert."

    def get_success_url(self):
        return reverse('projectarchive:details', kwargs={'pk': self.object.id})


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    model = Projectarticle
    success_url = "/projectarchive/"
    permission_required = "projectarchive.delete_article"


