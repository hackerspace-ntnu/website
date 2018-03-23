from django.conf.urls import url
from . import views

app_name = 'userprofile'

urlpatterns = [
    url(r'^members/$', views.members),
    url(r'^$', views.profile, name='profile'),
    url(r'^(?P<profile_id>[0-9]+)$', views.specific_profile, name='profile_by_id'),
    url(r'^edit', views.edit_profile, name="edit_profile"),
    url(r'^skill/(?P<skill_title>.+)$', views.skill, name='skill')
]
