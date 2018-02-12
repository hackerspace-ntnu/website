from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.coffee_pot, name='coffee_post'),
    url(r'^get_status/?(?P<pot>\w+)$', views.get_coffee, name='get_coffee'),
    url(r'^get_json/', views.get_json, name='get_coffee_json'),
    url(r'^door-data/', views.coffee_data, name='coffee_data'),
    url(r'^chart/', views.coffee_chart, name='coffee_chart'),
]
