from django.conf.urls import url


from authentication import views

urlpatterns = [
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^change-password/$', views.change_password, name='change_password'),
    url(r'^change-password-done/$', views.change_password_done, name='change_password_done'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup-done/$', views.signup_done, name='signup_done'),
    url(r'^forgot-password/$', views.forgot_password, name='forgot_password'),
    url(r'^forgot-password-done/$', views.forgot_password_done, name='forgot_password_done'),
    url(r'^activate/(?P<hash_key>[0-9a-zA-Z]+)/$', views.activate_account, name='activate_account'),
    url(r'set-password-done', views.set_password_done, name='set_password_done'),

]
