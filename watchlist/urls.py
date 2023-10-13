from django.urls import path

from website.urls import api_router

from .views import shift_slot, template_views

app_name = "watchlist"
api_router.register("shiftslots", shift_slot.ShiftSlotViewSet)

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
]
