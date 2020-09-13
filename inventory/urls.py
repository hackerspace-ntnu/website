from .models import Asset
from django.urls import include, path
from .views import LinkPlaceShelf

app_name = "inventory"

urlpatterns = [
  path('LinkPlaceShelf/', LinkPlaceShelf.as_view(model=Asset), name='Asset_Place_Shelf_Link'),
]