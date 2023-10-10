from typing import Any, Dict

from rest_framework import serializers

from applications.models import Application, ApplicationGroupChoice
from applications.serializers.application_group import ApplicationGroupSerializer


class ApplicationListSerializer(serializers.ModelSerializer):

    group_choice = ApplicationGroupSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = (
            "id",
            "name",
            "email",
            "group_choice",
        )

    def create(self, validated_data: Dict[str, Any], *args, **kwargs):
        groups = validated_data.pop("group_choice")
        application = super().create(validated_data, *args, **kwargs)

        for group in groups:
            ApplicationGroupChoice.objects.create(**group, application=application)

        return application

    def update(self, instance, validated_data):
        groups = validated_data.pop("group_choice")
        ApplicationGroupChoice.objects.delete(application=instance)
        for group in groups:
            ApplicationGroupChoice.objects.create(**group, application=instance)

        return super().update(instance, validated_data)


class ApplicationRetrieveSerializer(ApplicationListSerializer):
    class Meta:
        model = Application
        fields = (
            "id",
            "name",
            "email",
            "phone",
            "study",
            "year",
            "knowledge_of_hs",
            "about",
            "application_text",
            "project_interests",
            "application_date",
            "group_choice",
        )
