from rest_framework import serializers
from .models import Item, Tag



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'parent_tag', 'item_set')
        depth = 2

class ItemSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset = Tag.objects.all())

    class Meta:
        model = Item
        fields = ('id','name','description', 'quantity', 'thumbnail', 'tags', 'zone', 'shelf', 'row', 'column')
        depth = 2
