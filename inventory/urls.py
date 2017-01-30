from django.conf.urls import url
from . import views

app_name = 'inventory'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^add_item/', views.add_item, name='add_item'),
    url(r'^(?P<item_id>[0-9]+)/add_item/$', views.add_item, name='add_item'),
    url(r'^(?P<item_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^change_multiple_items/', views.change_multiple_items, name='change_multiple_items'),

    url(r'^add_tag/', views.add_tag, name='add_tag'),
    url(r'^(?P<tag_id>[0-9]+)/add_tag/$', views.add_tag, name='add_tag'),
    url(r'^(?P<tag_id>[0-9]+)/tag_detail/$', views.tag_detail, name='tag_detail'),

    url(r'^register_loan/', views.register_loan, name='register_loan'),
    url(r'^administrate_loans/', views.administrate_loans, name='administrate_loans'),
    url(r'^loan_detail/(?P<loan_id>[0-9]+)/$', views.loan_detail, name='loan_detail'),
    url(r'^my_loans/', views.my_loans, name='my_loans'),

    url(r'^search/', views.search, name='search'),
]
