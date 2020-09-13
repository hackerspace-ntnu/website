from django.shortcuts import render
from .models import Shelf
from dal import autocomplete


class LinkPlaceShelf(autocomplete.Select2QuerySetView):
  def get_queryset(self):
    qs = Shelf.objects.all()
    Place = self.forwarded.get('place', None)
    if Place:
      qs = qs.filter(place_id=Place)

    if self.q:
      qs = qs.filter(name__icontains=self.q)

    return qs