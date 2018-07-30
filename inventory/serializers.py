from rest_framework import serializers
from .models import Item, Tag, Loan


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id','name','description', 'quantity', 'thumbnail', 'tags', 'zone', 'shelf', 'row', 'column', 'loans', 'quantity_left')


class TagSerializer(serializers.ModelSerializer):
    item_set = ItemSerializer(many=True, read_only=True)
    class Meta:
        model = Tag
        fields = ('id', 'name', 'item_set')
        depth = 2


class LoanSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Item.objects.all())
    class Meta:
        model = Loan
        fields = ('id', 'comment',
                  'email', 'phone', 'item', 'quantity')
        depth = 2
