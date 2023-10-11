from rest_framework import serializers

from news.models import Article


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "ingress_content",
            "internal",
            "pub_date",
            "thumbnail",
        )


class ArticleRetrieveSerializer(ArticleListSerializer):
    class Meta:
        model = Article
        fields = "__all__"
