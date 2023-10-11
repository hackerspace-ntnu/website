from rest_framework import serializers

from inventory.models.item import Item


class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            "id",
            "name",
            "stock",
            "unknown_stock",
            "can_loan",
            "thumbnail",
            "location",
        )


class ItemRetrieveSerializer(ItemListSerializer):
    class Meta(ItemListSerializer.Meta):
        fields = ItemListSerializer.Meta.fields + (
            "description",
            "max_loan_duration",
            "views",
        )
