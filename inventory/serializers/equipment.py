from rest_framework import serializers

from inventory.models.equipment import Equipment


class EquipmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = (
            "name",
            "inventory_link",
            "thumbnail",
        )


class EquipmentRetrieveSerializer(EquipmentListSerializer):
    class Meta(Equipment.Meta):
        fields = EquipmentListSerializer.Meta.fields + ("description",)
