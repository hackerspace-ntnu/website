from rest_framework import serializers

from applications.models import ApplicationGroup


class ApplicationGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationGroup
        fields = "__all__"
