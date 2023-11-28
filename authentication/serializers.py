from django.contrib.auth.models import Group, User
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)


class UserSerializer(serializers.ModelSerializer):

    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "groups")
