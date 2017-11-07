from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='list_all'),
    url(r'^(?P<name>[\w-]+)/', include([
        url(r'^$',  views.view_committee, name='view'),
    ])),
    url(r'^edit_members/(?P<committee_name>[\w-]+)/', views.edit_members, name='edit_members')
]
