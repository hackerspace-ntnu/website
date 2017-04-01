from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from .models import Tag, Item
from datetime import datetime
import json


def quantity_validator(number):
    if int(number) > 0:
        return number
    else:
        raise ValidationError(_("Antall kan ikke være negativt."), code='Invalid')


class ItemForm(forms.Form):
    name = forms.CharField(label='Gjenstand', max_length=100, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    description = forms.CharField(widget=forms.Textarea, label='Beskrivelse', max_length=300, strip=True,
                                  required=False)
    quantity = forms.IntegerField(label='Antall', validators=[quantity_validator], required=False)
    tags = forms.CharField(required=False)
    tags_chips = forms.CharField(widget=forms.HiddenInput, required=False)

    # Felt for plassering i rommet.
    zone = forms.CharField(required=False, label='Sone')
    shelf = forms.IntegerField(required=False, label='Hylle')
    place = forms.IntegerField(required=False, label='Plass')

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
        """ Sets the visible field to False
        Args:
            items: id's separated with '_' (also at the end)
        """
        for item_id in items.split('_'):
            if item_id:
                item = get_object_or_404(Item, pk=item_id)
                item.visible = False
                item.save()

    @staticmethod
    def change_tags(items_str: str, new_tags: str):
        """ Updates the tags for items in item_str to the tags in new_tags
        Args:
            items_str, new_tags: id's separated with '_' (also at the end)
        """
        tags = [get_object_or_404(Tag, pk=tag_id) for tag_id in new_tags.split('_')[:-1]]
        items = [get_object_or_404(Item, pk=item_id) for item_id in items_str.split('_')[:-1]]
        for item in items:
            item.tags.remove(*item.tags.all())
            item.tags.add(*tags)
            item.save()

    def clean(self):
        cleaned_data = super(ItemForm, self).clean()
        """Splitter alle nye tags i 'tags' feltet og legger strengene tilbake i cleaned data"""
        delimiter = ','
        new_tags = cleaned_data['tags']
        all_tags = []
        if new_tags:
            tags_list = new_tags.split(delimiter)
            for new_tag in tags_list:
                all_tags.append(new_tag.strip())
        cleaned_data['tags'] = all_tags
        return cleaned_data

    def add_new_tags(self, item_id):
        tag_dict = dict((tag.name.lower(), tag) for tag in Tag.objects.all())
        item = Item.objects.get(pk=item_id)
        for old_tag in item.tags.all():
            item.tags.remove(old_tag)
        for tag_id in self.cleaned_data['tags_chips'].split():
            # tags_chips is ids from eventually already existing tags (can be seen as chips when changing an item).
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
        self.add_parent_tags(item)

    @staticmethod
    def add_parent_tags(item):
        """
        Legger til alle tags som er foreldre til denne item sine tags, som tags på dette item objektet.
        """
        for tag in item.tags.all()[:]:
            for grand_tag in ItemForm.get_parent_tags(tag):
                item.tags.add(grand_tag)
                item.save()

    @staticmethod
    def get_parent_tags(tag):
        """
        :param tag:
        :return: liste med alle tags som ligger over tag i hierarkiet.
        """
        if tag.parent_tag is not None:
            return [tag.parent_tag, *ItemForm.get_parent_tags(tag.parent_tag)]
        else:
            return []


class TagForm(forms.Form):
    name = forms.CharField(label='Tag', max_length=100, strip=True,
                           widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    parent_tag = forms.CharField(label='Parent tag', max_length=100, strip=True, required=False,
                                 widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    # For å sende inn id til chips automatisk ved post.
    parent_tag_ids = forms.CharField(widget=forms.HiddenInput, max_length=100, strip=True, required=False)

    @staticmethod
    def add_parent_tag(tag_id, parent_tag_id):
        """
        Legger til parent_tag til tag, og flytter alle items som blir påvirket.

        - Registerer så alle items som har tag som tag, til også å være registrert med
          parent_tag som tag.

        - Hvis tag har en parent_tag fra før:
            -  Man skifter til en ny parent_tag
                -  Alle items som var tagget med parent_tag OG tag, må fjerne parent_tag fra tagger.

            -  Man fjerner parent tag (setter taggen øverst i treet).

        """
        def add_or_remove_tags_from_items(tag, method_str):
            """
            Legger til/fjerner alle tags som er over tag i hierarkiet fra alle items som er tagget med tag.
            :param tag:
            :param method_str: 'add' or 'remove'
            """
            for item in tag.item_set.all():
                method = getattr(item.tags, method_str)
                method(*ItemForm.get_parent_tags(tag))
                item.save()

        tag = Tag.objects.get(pk=tag_id)
        if parent_tag_id == '':
            # Man vil fjerne eksisterende parent_tag, eller bare fortsette å ikke ha noen.
            if tag.parent_tag is None:
                # Tag har INGEN parent_tag fra før, ingenting skal skje.
                pass

            else:
                # Tag har en parent_tag fra før
                # Alle items som har tag, må få fjernet parent_tag fra tagger.
                # MÅ også fjerne parent_tag sin parent_tag osv fra item tagger.

                add_or_remove_tags_from_items(tag, 'remove')
                tag.parent_tag = None
                tag.save()
        else:
            # Man skal sette ny parent tag
            parent_tag = Tag.objects.get(pk=parent_tag_id)

            if tag.parent_tag is None:
                # Tag har INGEN parent_tag fra før
                tag.parent_tag = parent_tag
                tag.save()
                parent_tag.item_set.add(*tag.item_set.all())

                add_or_remove_tags_from_items(tag, 'add')

            else:
                # Tag har en parent_tag fra før. Må fjerne alle gamle tags som ligger over i hierarkiet, og legge til
                # alle som ligger over i det nye.
                add_or_remove_tags_from_items(tag, 'remove')
                tag.parent_tag = parent_tag
                tag.save()
                add_or_remove_tags_from_items(tag, 'add')


class LoanForm(forms.Form):
    """
    items = forms.CharField(label='Gjenstand', max_length=100, widget=forms.TextInput(attrs={'autocomplete': 'off'}),
                            strip=True)
    """
    items = forms.CharField(label='Gjenstand', max_length=100, widget=forms.HiddenInput, strip=True)

    borrower = forms.CharField(label='Brukernavn lånetaker', max_length=100, strip=True)  # username
    comment = forms.CharField(widget=forms.Textarea(attrs={'autocomplete': 'off'}), label='Beskrivelse',
                              max_length=300,
                              strip=True,
                              required=False)
    return_date = forms.CharField(label='Returdato', widget=forms.HiddenInput)

    @staticmethod
    def delete_loan(loan):
        loan.visible = False
        loan.save()

    @staticmethod
    def get_autocomplete_dict():
        dic = {}
        for item in Item.objects.all():
            item_name = item.name
            item_dict = {
                'id': item.id,
                'text': item_name,
            }
            for i in range(1, len(item_name) + 1):
                try:
                    dic[item_name[0:i].upper()].append(item_dict)
                except KeyError:
                    dic[item_name[0:i].upper()] = [item_dict]
        return json.dumps(dic)

    def clean(self):
        cleaned_data = super(LoanForm, self).clean()

        # ITEM
        delimiter = ','
        try:
            item_ids_string = cleaned_data['items']  # int
        except KeyError:
            raise ValidationError({'items': "Ingen items i feltet"})
        else:
            if item_ids_string[-1] == delimiter:
                item_ids_string = item_ids_string[:-1]

        try:
            # skjekk at feltet består av tall separert av delimiter
            item_ids = list(map(int, item_ids_string.split(delimiter)))
        except ValueError:
            raise ValidationError({'items': "MÅ RETURNERES SOM TALL ADSKILT MED {}".format(delimiter)})
        else:
            item_list = []
            for item_id in item_ids:
                try:
                    item = Item.objects.get(pk=item_id)
                except Item.DoesNotExist:
                    raise ValidationError({'items': "En av item id'ene eksisterer ikke."}, code='Invalid')
                else:
                    item_list.append(item)
            else:
                cleaned_data['items'] = item_list

        # BORROWER
        borrower_string = cleaned_data['borrower']  # String with only username.
        user_query = User.objects.filter(username=borrower_string)
        if len(user_query) != 1:
            raise ValidationError({'borrower': "Feil med brukernavn upps."}, code='Error')
        else:
            borrower = user_query[0]
        cleaned_data['borrower'] = borrower

        # COMMENT
        comment = cleaned_data['comment']
        if not comment:
            del cleaned_data['comment']

        # RETURN_DATE
        # string format: DD Month, YYYY
        return_date_string = cleaned_data['return_date'] + " 18:00"  # default time for return
        return_date = datetime.strptime(return_date_string, "%d %B, %Y %H:%M")
        cleaned_data['return_date'] = return_date

        return cleaned_data
