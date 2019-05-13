from django.urls import path
from authentication.views import LoginView, LogoutView


app_name = 'auth'

urlpatterns = [
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
]
