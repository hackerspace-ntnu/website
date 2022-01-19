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

# Fjerne internal senere
    def get_internal_articles_indicator(self):

        if not self.request.user.has_perm('projectarchive.can_view_internal_article'):
            return "Du har ikke rettigheter til å se interne artikler."

        return None


    def get_queryset(self):
        # Retrieve published articles (so no drafts)
        articles = Projectarticle.objects.order_by('-pub_date').filter(draft=False)

# Fjerne internal seneter
        # Decide if visitor should see internal articles
        if self.request.user.has_perm("projectarchive.can_view_internal_article"):
            return articles
        else:
            return articles.filter(internal=False)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

# Fjerne internal senere
        context['indicator_text'] = self.get_internal_articles_indicator()

        # Retrieve any user drafts if logged in
        if self.request.user.has_perm("projectarchive.add_article"):
            context['drafts'] = Projectarticle.objects.order_by('-pub_date').filter(author=self.request.user,draft=True)

        return context


class ArticleView(DetailView):
    model = Projectarticle
    template_name = "projectarchive/article.html"

    def dispatch(self, request, *args, **kwargs):

        article = self.get_object()

# Fjerne internal senere
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

# Fjerne internal senere
        # Check user internal article view permission
        can_access_internal_article = self.request.user.has_perm('projectarchive.can_view_internal_article')

# Fjerne internal senere
        # Get permitted articles
        article_list = Projectarticle.objects.filter(internal__lte=can_access_internal_article,draft=False)

        # Get oldest article that is newer than current (None if current is latest)
        next_article = article_list.filter(pub_date__gt=self.get_object().pub_date).order_by('pub_date').first()

        # Get latest article that is older than current (None if current is oldest)
        previous_article = article_list.filter(pub_date__lt=self.get_object().pub_date).order_by('-pub_date').first()

        context['next_article'] = next_article
        context['previous_article'] = previous_article

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


