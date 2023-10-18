from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import shift_slot, template_views

api_router = DefaultRouter()
api_router.register("shift-slots", shift_slot.ShiftSlotViewSet, basename="shift-slots")

app_name = "watchlist"

urlpatterns = [
    path("", template_views.watchlistView.as_view(), name="vaktliste"),
    path(
        "register/<int:pk>",
        template_views.WatchListRegisterView.as_view(),
        name="register",
    ),
    path(
        "unregister/<int:pk>",
        template_views.WatchListUnregisterView.as_view(),
        name="unregister",
    ),
    path("reset", template_views.WatchListResetView.as_view(), name="reset"),
    path("api/", include(api_router.urls)),
]
