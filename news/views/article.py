from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from news.filters.article import ArticleFilter
from news.models import Article
from news.serializers.article import ArticleListSerializer, ArticleRetrieveSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleListSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = ArticleFilter
    search_fields = [
        "title",
        "ingress_content",
        "main_content",
        "author__first_name",
        "author__last_name",
    ]

    def create(self, request, *args, **kwargs):
        request.data["author"] = request.user.id
        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "list":
            return ArticleListSerializer
        return ArticleRetrieveSerializer

    def get_queryset(self):
        queryset = Article.objects.all().order_by("-pub_date")
        user = self.request.user
        include_internal = user and user.has_perm("news.can_view_internal_article")
        if include_internal:
            queryset = Article.objects.all()
        else:
            queryset = Article.objects.filter(internal=False)
        return queryset
