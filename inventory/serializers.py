from rest_framework import serializers
from .models import Item, Tag


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id','name','description', 'quantity', 'thumbnail', 'tags', 'zone', 'shelf', 'row', 'column')

class TagSerializer(serializers.ModelSerializer):
    item_set = ItemSerializer(many=True)
    class Meta:
        model = Tag
        fields = ('id', 'name', 'parent_tag', 'item_set')
        depth = 2
