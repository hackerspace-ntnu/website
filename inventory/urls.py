from django.conf.urls import url
from django.contrib.auth.decorators import permission_required
from . import views

app_name = 'inventory'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^change_multiple_items/', views.change_multiple_items, name='change_multiple_items'),
    url(r'^register_loan/(?P<item_id>[0-9]+)/$',
        permission_required('inventory.add_loan')(views.RegisterLoan.as_view()), name='register_loan'),
    url(r'^administrate_loans/', views.administrate_loans, name='administrate_loans'),
    url(r'^loan_detail/(?P<loan_id>[0-9]+)/$', views.loan_detail, name='loan_detail'),
    url(r'^my_loans/', views.my_loans, name='my_loans'),
    url(r'^search/', views.search, name='search'),
]
