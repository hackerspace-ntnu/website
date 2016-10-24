from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^(?P<name>\w+)/$',views.detail,name="detail"),
    url(r'^add$',views.addRPI,name="addrpi"),
    url(r'^lifesign',views.lifesign,name='dontdieonme')
]
