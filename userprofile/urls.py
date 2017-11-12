from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.members),
    url(r'^profile/(?P<profileID>[0-9]+)$', views.profile, name='profile'),
    url(r'^edit_profile/(?P<profileID>[0-9]+)$', views.edit_profile_id),
    url(r'^edit_profile', views.edit_profile),
    #url(r'^viewGroup/', views.group),
    url(r'^viewSkill/(?P<skill_title>.+)$', views.skill)
]
