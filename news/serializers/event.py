from rest_framework import serializers

from news.models import Event


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = fields = (
            "id",
            "title",
            "ingress_content",
            "internal",
            "pub_date",
            "thumbnail",
        )


class EventRetrieveSerializer(EventListSerializer):
    class Meta:
        model = Event
        fields = "__all__"
