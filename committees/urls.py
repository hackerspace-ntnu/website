from django.conf.urls import include, url

from . import views

app_name = 'committees'

urlpatterns = [
    url(r'^$', views.index, name='list_all'),
    url(r'^index/$', views.index, name='list_all'),
    url(r'^(?P<slug>[\w-]+)/', include([url(r'^$',  views.ViewCommittee.as_view(), name='view_committee'),])),
    url(r'^(?P<committee_name>[\w-]+)/edit_members/', views.edit_members, name='edit_members'),
    url(r'^(?P<committee_name>[\w-]+)/edit/', views.edit_committee, name='edit_committee')
]

