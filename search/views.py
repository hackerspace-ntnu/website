from itertools import chain

from django.views.generic import ListView

from news.models import Article
from projectarchive.models import Projectarticle
from userprofile.models import Profile


class SearchView(ListView):
    template_name = "search/view.html"
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["query"] = self.request.GET.get("q")
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get("q", None)

        if query is not None:
            article_results = Article.objects.search(query)
            project_article_results = Projectarticle.objects.search(query)
            profile_results = Profile.objects.search(query)

            queryset_chain = chain(
                article_results,
                project_article_results,
                profile_results,
            )

            queryset = sorted(
                queryset_chain, key=lambda instance: instance.pk, reverse=True
            )
            self.count = len(queryset)
            return queryset
        return Article.objects.none()  # some empty queryset
