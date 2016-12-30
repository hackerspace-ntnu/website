from django.shortcuts import get_object_or_404
from django import forms

from .models import Tag, Item
import json


class ItemForm(forms.Form):
    name = forms.CharField(label='Gjenstand', max_length=100, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    # description = forms.CharField(label='Beskrivelse', max_length=300, strip=True, required=False)
    description = forms.CharField(widget=forms.Textarea, label='Beskrivelse', max_length=300, strip=True,
                                  required=False)
    quantity = forms.IntegerField(label='Antall')
    tags = forms.CharField(required=False)
    tags_chips = forms.CharField(widget=forms.HiddenInput, required=False)

    @staticmethod
    def get_autocomplete_dict():
        dic = {}
        for tag in Tag.objects.all():
            tag_name = tag.name
            tag_dict = {
                'id': tag.id,
                'text': tag_name,
            }
            for i in range(1, len(tag_name) + 1):
                try:
                    dic[tag_name[0:i].upper()].append(tag_dict)
                except KeyError:
                    dic[tag_name[0:i].upper()] = [tag_dict]
        return json.dumps(dic)

    @staticmethod
    def delete_all_items(items: str):
        """ Deletes all the items
        Args:
            items: id's separated with '_' (also at the end)
        """
        # TODO legge inn en slags barnesikring på sletting? her kunne det vært praktisk med en property for synlig/ikke
        for item_id in items.split('_'):
            if item_id:
                item = get_object_or_404(Item, pk=item_id)
                item.delete()

    @staticmethod
    def change_tags(items_str: str, new_tags: str):
        """ Updates the tags for items in item_str to the tags in new_tags
        Args:
            items_str, new_tags: id's separated with '_' (also at the end)
        """
        tags = [Tag.objects.get(pk=tag_id) for tag_id in new_tags.split('_')[:-1]]
        items = [Item.objects.get(pk=item_id) for item_id in items_str.split('_')[:-1]]
        for item in items:
            for old_tag in item.tags.all():
                item.tags.remove(old_tag.id)
            item.tags.add(*tags)
            item.save()

    def clean(self):
        # super(ItemForm, self).clean()
        """Splitter alle nye tags i 'tags' feltet og legger strengene tilbake i cleaned data"""
        delimiter = ','
        new_tags = self.cleaned_data['tags']
        all_tags = []
        if new_tags:
            tags_list = new_tags.split(delimiter)
            for new_tag in tags_list:
                all_tags.append(new_tag.strip())
        self.cleaned_data['tags'] = all_tags

    def add_new_tags(self, item_id):
        tag_dict = dict((tag.name.lower(), tag) for tag in Tag.objects.all())
        item = Item.objects.get(pk=item_id)
        for old_tag in item.tags.all():
            item.tags.remove(old_tag)
        for tag_id in self.cleaned_data['tags_chips'].split():
            tag_id = tag_id.strip()
            item.tags.add(Tag.objects.get(pk=tag_id))
        for new_tag in self.cleaned_data['tags']:
            try:
                # check if new_tag already exist
                tag = tag_dict[new_tag.strip().lower()]
                item.tags.add(tag)
            except KeyError:
                # make new tag and add to item.tags
                tag = Tag(name=new_tag)
                tag.save()
                item.tags.add(tag)
        item.save()


class TagForm(forms.Form):
    name = forms.CharField(label='Tag', max_length=100, strip=True,
                           widget=forms.TextInput(attrs={'autocomplete': 'off'}))


class LoanForm(forms.Form):
    borrower = forms.CharField(label='Lånetaker', max_length=100, strip=True)  # username
    # den som låner ut gis implisitt etter hvem som er innlogget
    comment = forms.CharField(label='Kommentar', max_length=300, strip=True)

    # loan date gis implisitt
    return_date = forms.DateField(label='Returdato')


if __name__ == '__main__':
    print("hei")
