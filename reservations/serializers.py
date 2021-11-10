import datetime

from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers

from reservations.models import Reservation


class PrivacyUserField(serializers.PrimaryKeyRelatedField):
    def get_attribute(self, instance):
        """
        Given the *outgoing* object instance, return the primitive value
        that should be used for this field.
        """
        if instance.user.id == self.context["request"].user.id:
            return super(PrivacyUserField, self).get_attribute(instance)
        return None


class PrivacyCharField(serializers.CharField):
    def get_attribute(self, instance):
        """
        Given the *outgoing* object instance, return the primitive value
        that should be used for this field.
        """
        if instance.user.id == self.context["request"].user.id:
            return super(PrivacyCharField, self).get_attribute(instance)
        return None


class ReservationsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")
    fullname = serializers.ReadOnlyField(source="user.get_full_name")
    phone = serializers.ReadOnlyField(source="user.profile.phone_number")

    class Meta:
        model = Reservation
        fields = (
            "start",
            "end",
            "user",
            "parent_queue",
            "comment",
            "id",
            "fullname",
            "phone",
        )

    def validate(self, attrs):
        # Updating comment requires PATCH
        if self.context["request"].method == "PATCH":
            # Allow comment update, ignore any other attributes
            return {"comment": attrs["comment"]}

        # Disallow reservations into the past, but be slightly forgiving
        now = datetime.datetime.now() - datetime.timedelta(minutes=15)
        if attrs["start"] == attrs["end"]:
            raise serializers.ValidationError(
                "Reservasjonen begynner samtidig som den slutter."
            )

        if attrs["start"] <= now:
            raise serializers.ValidationError("Du kan ikke reservere i fortiden.")

        # Disallow weekend and late/early hour reservations to non-members
        user = self.context["request"].user
        if (
            not user.has_perm("reservations.view_user_details")
            and not user.is_superuser
        ):
            if (
                attrs["start"].time().hour < 10
                or attrs["end"].time().hour > 18
                or attrs["start"].date().weekday() >= 6
                or attrs["end"].date().weekday() >= 6
                or attrs["start"].date() != attrs["end"].date()
            ):
                raise serializers.ValidationError(
                    "Non-members are not allowed to make reservations outside opening hours"
                )

        # Check if the new reservation conflicts with any of the old ones in the same queue
        # note that Fullcalendar allows reservations across multiple days, but not across multiple weeks
        reservations = Reservation.objects.filter(
            parent_queue_id=attrs["parent_queue"]
        ).all()

        for r in reservations:
            # Hvis nye eventen har start tid inni en annen
            if r.start <= attrs["start"] <= r.end:
                raise serializers.ValidationError(
                    "Valgt starttid overlapper med annen reservasjon."
                )
            # Hvis den nye eventen har slutt-tid inni en annen
            elif r.start <= attrs["end"] <= r.end:
                raise serializers.ValidationError(
                    "Valgt slutttid overlapper med annen reservasjon."
                )
            elif (attrs["start"] <= r.start) and (attrs["end"] >= r.end):
                raise serializers.ValidationError(
                    "Valgt start og slutttid overlapper med annen reservasjon."
                )

        # Specify the reservee here instead of in the request (to prevent someone from reserving for someone else...)
        attrs["user"] = self.context["request"].user

        return attrs
