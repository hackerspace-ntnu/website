from django.conf.urls import url
from . import views

app_name = 'inventory'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<item_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^add_item/', views.add_item, name='add_item'),  # TODO
    url(r'^(?P<item_id>[0-9]+)/add_item/$', views.add_item, name='add_item'),

    url(r'^add_tag/', views.add_tag, name='add_tag'),  # TODO
    url(r'^(?P<tag_id>[0-9]+)/add_tag/$', views.add_tag, name='add_tag'),
    url(r'^(?P<tag_id>[0-9]+)/tag_detail/$', views.tag_detail, name='tag_detail'),

    url(r'^loan/', views.loan, name='loan'),
    url(r'^registered/', views.registered, name='registered'),

    url(r'^search/', views.search, name='search'),
]
