from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^image/(?P<title>[0-9]+)/$', views.image, name='image'),
    url(r'^images/', views.ImageListView.as_view(), name='images'),
    url(r'^image-upload/', views.imageUpload, name='image-upload'),
    url(r'^image-delete/(?P<pk>[0-9]+)', views.ImageDeleteView.as_view(), name='image-delete'),
    url(r'^image-newest/', views.ajax_return_last_image, name='recent-upload'),
    url(r'^image/(?P<image_id>[0-9]+)/view', views.imageView, name='image'),
]
