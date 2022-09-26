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

        can_access_internal_article = self.request.user.has_perm(
            "news.can_view_internal_article"
        )
        can_access_internal_event = self.request.user.has_perm(
            "news.can_view_internal_event"
        )
        can_access_internal_rule = self.request.user.has_perm(
            "website.can_view_internal_rule"
        )

        if query is not None:
            article_results = Article.objects.search(query).filter(
                internal__lte=can_access_internal_article, draft=False
            )
            project_article_results = Projectarticle.objects.search(query).filter(
                draft=False
            )
            event_results = Event.objects.search(query).filter(
                internal__lte=can_access_internal_event, draft=False
            )
            profile_results = Profile.objects.search(query)
            queue_results = Queue.objects.search(query)
            faq_results = FaqQuestion.objects.search(query)
            rule_results = Rule.objects.search(query).filter(
                internal__lte=can_access_internal_rule
            )

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
