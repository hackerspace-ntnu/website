from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('images/', views.ImageListView.as_view(), name='images'),
    path('image-upload/', views.imageUpload, name='image-upload'),
    path('image-delete/<int:pk>', views.ImageDeleteView.as_view(), name='image-delete'),
    path('image-view/<int:pk>', views.ImageView.as_view(), name='image-detail'),
]
