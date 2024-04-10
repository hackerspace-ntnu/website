from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ArticleForm
from .models import Projectarticle


class ArticleListView(ListView):
    Model = Projectarticle
    template_name = "projectarchive/projectarchive.html"
    paginate_by = 10

    def get_queryset(self):
        # Retrieve published articles (so no drafts)
        articles = Projectarticle.objects.order_by("-pub_date").filter(draft=False)

        return articles

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # Retrieve any user drafts if logged in
        if self.request.user.has_perm("projectarchive.add_projectarticle"):
            context["drafts"] = Projectarticle.objects.order_by("-pub_date").filter(
                author=self.request.user, draft=True
            )

        return context


class ArticleView(DetailView):
    model = Projectarticle
    template_name = "projectarchive/article.html"

    def dispatch(self, request, *args, **kwargs):

        article = self.get_object()

        # If the article is a draft, check if user is the author
        if article.draft and not request.user == article.author:

            # Stores log-in prompt message to be displayed with redirect request
            messages.add_message(
                request, messages.WARNING, "Du har ikke tilgang til artikkelen"
            )

            return redirect("/")

        return super(ArticleView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        return context


class ArticleCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Projectarticle
    form_class = ArticleForm
    template_name = "projectarchive/edit_article.html"
    permission_required = "projectarchive.add_projectarticle"

    def get_success_message(self, cleaned_data):
        if self.object.draft:
            return "Artikkelen er opprettet som utkast"
        return "Artikkelen er opprettet og publisert"

    def get_success_url(self):
        return reverse("projectarchive:details", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Projectarticle
    form_class = ArticleForm
    template_name = "projectarchive/edit_article.html"
    permission_required = "projectarchive.change_projectarticle"
    success_message = "Artikkelen er oppdatert."

    def get_success_url(self):
        return reverse("projectarchive:details", kwargs={"pk": self.object.id})


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    model = Projectarticle
    success_url = reverse_lazy("projectarchive:Article_List")
    permission_required = "projectarchive.delete_projectarticle"
