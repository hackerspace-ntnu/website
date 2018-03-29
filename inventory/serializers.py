from rest_framework import serializers
from .models import Item, Tag, Loan


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id','name','description', 'quantity', 'thumbnail', 'tags', 'zone', 'shelf', 'row', 'column')


class TagSerializer(serializers.ModelSerializer):
    item_set = ItemSerializer(many=True, read_only=True)
    class Meta:
        model = Tag
        fields = ('id', 'name', 'item_set')
        depth = 2


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ('id', 'borrower', 'lender', 'comment')
        depth = 2
