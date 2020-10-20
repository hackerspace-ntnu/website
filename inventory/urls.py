from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.InventoryListView.as_view(), name='inventory'),
    path('item/<int:pk>', views.ItemDetailView.as_view(), name='item'),
]
