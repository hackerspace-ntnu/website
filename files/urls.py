from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^image/(?P<title>[0-9]+)/$', views.image, name='image'),
    url(r'^images/$', views.images, name='images'),
    url(r'^image-upload/$', views.imageUpload, name='image-upload'),
    url(r'^image/(?P<image_id>[0-9]+)/delete', views.imageDelete, name='image-delete'),
    url(r'^image/(?P<image_id>[0-9]+)/edit', views.imageEdit, name='image-edit'),
    url(r'^image/(?P<image_id>[0-9]+)/view', views.imageView, name='image-view'),
]
