from rest_framework import serializers
from .models import Item, Tag


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id','name','description', 'quantity', 'thumbnail', 'tags', 'zone', 'shelf', 'row', 'column')
        depth = 2

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'parent_tag', 'item_set')
        depth = 2
