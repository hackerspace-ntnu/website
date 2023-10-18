from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework import viewsets

from news.models import Article
from news.serializers.article import ArticleListSerializer, ArticleRetrieveSerializer


class ArticleViewSet(viewsets.ModelViewSet, PermissionRequiredMixin):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ArticleListSerializer
        return ArticleRetrieveSerializer

    permission_required = "can_view_internal_article"
