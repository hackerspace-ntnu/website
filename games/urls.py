from django.urls import path
from . import views

#TODO: No urls should point here for any purposes other than testing

urlpatterns = [
    path('', views.GameView.as_view(), name='games'),
]
