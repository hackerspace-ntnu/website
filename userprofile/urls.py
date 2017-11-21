from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.members),
    url(r'^(profile/)?(?P<profileID>[0-9]+)$', views.profile, name='profile'),
    url(r'^(profile/)?(?P<profileID>[0-9]+)/edit$', views.edit_profile_id),
    url(r'^edit', views.edit_profile),
    #url(r'^viewGroup/', views.group),
    url(r'^skill/(?P<skill_title>.+)$', views.skill)
]
