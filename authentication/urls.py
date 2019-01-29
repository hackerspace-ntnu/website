from django.urls import path
from django.contrib.auth.views import logout as legacy_logout

from . import views

app_name = 'auth'

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('login_callback', views.login_callback, name='login_callback'),
    path('logout_legacy', legacy_logout, name="legacy_logout")
]
