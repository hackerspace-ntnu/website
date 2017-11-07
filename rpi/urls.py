from django.conf.urls import url

from rpi.views import RPiListView, RPiAPIView

urlpatterns = [
    url(r'^$', RPiListView.as_view(), name='rpi'),
    url(r'^api/', RPiAPIView.as_view(), name='rpi-api'),
]
