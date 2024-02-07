from rest_framework import serializers

from authentication.serializers.user import UserProfileDetailSerializer
from news.models import Article


class ArticleListSerializer(serializers.ModelSerializer):

    author = UserProfileDetailSerializer(read_only=True)

    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "ingress_content",
            "internal",
            "pub_date",
            "thumbnail",
            "author",
        )


class ArticleRetrieveSerializer(ArticleListSerializer):
    class Meta:
        model = Article
        fields = "__all__"
