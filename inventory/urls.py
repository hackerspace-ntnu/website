from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.InventoryListView.as_view(), name='inventory'),
    path('item/<int:pk>', views.ItemDetailView.as_view(), name='item'),
    path('new', views.ItemCreateView.as_view(), name='new'),
    path('edit/<int:pk>', views.ItemUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>', views.ItemDeleteView.as_view(), name='delete'),
]
