from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.members),
    url(r'^profile/', views.profile),
    url(r'^edit_profile/', views.edit_profile),
    url(r'^viewGroup/', views.group)
]
