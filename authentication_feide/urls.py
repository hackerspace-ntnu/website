from django.conf.urls import url

from . import views

app_name = 'authentication_feide'

urlpatterns = [
    url(r'^$', views.index, name='feide_index'),
    url(r'^login$', views.login, name='login'),
    url(r'^login_callback', views.login_callback, name='login_callback'),
]
