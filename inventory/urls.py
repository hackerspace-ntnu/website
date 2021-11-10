from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path("", views.InventoryListView.as_view(), name="inventory"),
    path("item/<int:pk>", views.ItemDetailView.as_view(), name="item"),
    path("new", views.ItemCreateView.as_view(), name="new"),
    path("edit/<int:pk>", views.ItemUpdateView.as_view(), name="edit"),
    path("delete/<int:pk>", views.ItemDeleteView.as_view(), name="delete"),
    path("loans/", views.ItemLoanListView.as_view(), name="loans"),
    path("loans/<int:pk>", views.ItemLoanDetailView.as_view(), name="loan_application"),
    path(
        "loans/approve/<int:pk>",
        views.ItemLoanApproveView.as_view(),
        name="loan_approve",
    ),
    path("loans/deny/<int:pk>", views.ItemLoanDeclineView.as_view(), name="loan_deny"),
    path(
        "loans/returned/<int:pk>",
        views.ItemLoanReturnedView.as_view(),
        name="loan_returned",
    ),
    path(
        "loans/apply/<int:pk>",
        views.ItemLoanApplicationView.as_view(),
        name="loan_apply",
    ),
]
