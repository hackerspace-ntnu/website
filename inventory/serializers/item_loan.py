from rest_framework import serializers

from inventory.models.item_loan import ItemLoan
from inventory.serializers.item import ItemListSerializer


class ItemLoanListSerializer(serializers.ModelSerializer):

    item = ItemListSerializer()

    class Meta:
        model = ItemLoan
        fields = (
            "id",
            "item",
            "amount",
            "loan_from",
            "loan_to",
            "approver",
        )


class ItemLoanCreateUpdateSerializer(ItemLoanListSerializer):
    class Meta(ItemLoanListSerializer.Meta):
        fields = "__all__"
