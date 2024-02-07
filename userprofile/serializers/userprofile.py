from rest_framework import serializers

from userprofile.models import Profile


class ProfileListSerializer(serializers.ModelSerializer):
    """Profile with user as username"""

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "image",
            "skills",
        )
        read_only_fields = (
            "user",
            "skills",
        )


class ProfileRetrieveSerializer(ProfileListSerializer):
    class Meta(ProfileListSerializer.Meta):
        fields = ProfileListSerializer.Meta.fields + (
            "social_discord",
            "social_steam",
            "social_battlenet",
            "social_git",
            "limit_social",
            "study",
            "acceptance_criteria",
            "accepted_tos",
            "phone_number",
            "show_email",
            "allergi_gluten",
            "allergi_gluten",
            "allergi_vegan",
            "allergi_annet",
        )
