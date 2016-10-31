from django.conf.urls import url
from . import views

app_name = 'inventory'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<item_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^add_item/', views.add_item, name='add_item'),  # TODO
    url(r'^add_tag/', views.add_tag, name='add_tag'),  # TODO
    url(r'^loan/', views.loan, name='loan'),
    url(r'^registered/', views.registered, name='registered'),
    url(r'^(?P<item_id>[0-9]+)/change_item/$', views.change_item, name='change_item'),
]
