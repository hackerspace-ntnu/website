from django.conf.urls import url


from authentication import views

urlpatterns = [
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^change-password/$', views.change_password, name='change_password'),
    url(r'^change-password-done/$', views.change_password_done, name='change_password_done'),
]
