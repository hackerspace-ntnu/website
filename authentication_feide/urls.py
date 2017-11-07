from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='feide_index'),
    url(r'^login$', views.login, name='login'),
    url(r'^login_callback', views.login_callback, name='login_callback'),
]
