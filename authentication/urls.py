from django.urls import path

from authentication.views import LogoutView

app_name = "auth"

urlpatterns = [
    path("logout", LogoutView.as_view(), name="logout"),
]
