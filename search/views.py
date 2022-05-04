from itertools import chain

from django.views.generic import ListView, TemplateView

from news.models import Article, Event
from projectarchive.models import Projectarticle
from reservations.models import Queue
from userprofile.models import Profile
from website.models import FaqQuestion, Rule


class SearchView(TemplateView):
    template_name = "search/view.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["query"] = self.request.GET.get("q", "")
        context["page"] = self.request.GET.get("p", 1)
        return context


class SearchAPIView(ListView):
    template_name = "search/search_results.html"
    paginate_by = 5
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["query"] = self.request.GET.get("q", "")
        context["page"] = self.request.GET.get("p", 1)
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get("q", None)

        if query is not None:
            article_results = Article.objects.search(query)
            project_article_results = Projectarticle.objects.search(query)
            event_results = Event.objects.search(query)
            profile_results = Profile.objects.search(query)
            queue_results = Queue.objects.search(query)
            faq_results = FaqQuestion.objects.search(query)
            rule_results = Rule.objects.search(query)

            queryset_chain = chain(
                article_results,
                project_article_results,
                event_results,
                profile_results,
                queue_results,
                faq_results,
                rule_results,
            )

            queryset = sorted(
                queryset_chain, key=lambda instance: instance.pk, reverse=True
            )
            self.count = len(queryset)
            return queryset
        return Article.objects.none()  # some empty queryset
