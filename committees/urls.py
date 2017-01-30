from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='list_all'),
    url(r'^edit', views.edit, name='edit'),
    url(
        r'^user-autocomplete/',
        views.UserAutocomplete.as_view(),
        name='user-autocomplete',
    ),
    url(r'^(?P<slug>[\w-]+)/', include([
        url(r'^$',  views.view_committee, name='view'),
        url(r'^edit/', views.edit_description, name='edit_desc'),
    ])),
]
