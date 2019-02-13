from django.urls import path
from django.contrib.auth.views import logout as legacy_logout

from . import views

app_name = 'auth'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('login_callback', views.LoginCallbackView.as_view(), name='login_callback'),
]
