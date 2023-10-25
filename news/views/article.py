from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from news.models import Article
from news.serializers.article import ArticleListSerializer, ArticleRetrieveSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return ArticleListSerializer
        return ArticleRetrieveSerializer
