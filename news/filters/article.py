from django_filters import FilterSet

from news.models import Article


class ArticleFilter(FilterSet):
    class Meta:
        model = Article
        fields = ("internal", "author", "pub_date", "draft")
