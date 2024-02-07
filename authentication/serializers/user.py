from django.contrib.auth.models import User
from rest_framework import serializers

from userprofile.serializers.userprofile import (
    ProfileListSerializer,
    ProfileRetrieveSerializer,
)


class UserSerializer(serializers.ModelSerializer):
    """User serializer with profile id."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "groups",
            "profile",
        )
        read_only_fields = ("username", "groups", "profile", "email")


class UserProfileDetailSerializer(UserSerializer):
    """Serializer with profile detail object."""

    profile = ProfileListSerializer(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("profile",)


class UserRetrieveSerializer(UserSerializer):
    """Serializer with user and profile detail object."""

    profile = ProfileRetrieveSerializer(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("profile",)
        read_only_fields = ("username", "groups", "profile", "email")
