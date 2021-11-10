from django.urls import path
from . import views

app_name = "watchlist"

urlpatterns = [
    path("", views.watchlistView.as_view(), name="vaktliste"),
    path("register/<int:pk>", views.WatchListRegisterView.as_view(), name="register"),
    path(
        "unregister/<int:pk>",
        views.WatchListUnregisterView.as_view(),
        name="unregister",
    ),
    path("reset", views.WatchListResetView.as_view(), name="reset"),
]
