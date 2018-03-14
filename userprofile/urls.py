from django.conf.urls import url
from . import views

app_name = 'userprofile'

urlpatterns = [
    url(r'^$', views.members),
    url(r'^profile/(?P<profile_id>[0-9]+)$', views.profile, name='profile'),
    url(r'^profile/(?P<profile_id>[0-9]+)/edit$', views.edit_profile_id, name='edit_profile'),
    url(r'^edit', views.edit_profile),
    url(r'^skill/(?P<skill_title>.+)$', views.skill, name='skill')
]
