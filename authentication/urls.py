from django.conf.urls import url
from django.contrib.auth import views as auth_views
from authentication.views import logout_user, SignUpView, SignUpDoneView, SignUpConfirmView
from website.settings import DEFAULT_FROM_MAIL


app_name = "auth"
urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(template_name="authentication/login.html"), name='login'),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^change-password/$', auth_views.PasswordChangeView.as_view(template_name="authentication/change_password.html"), name='password_change'),
    url(r'^change-password-done/$', auth_views.PasswordChangeDoneView.as_view(template_name="authentication/redirection_page.html"), name='password_change_done'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^signup-done/$', SignUpDoneView.as_view(), name='signup_done'),
    url(r'^signup-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', SignUpConfirmView.as_view(), name='signup_confirm'),
    url(r'^forgot-password/$', auth_views.PasswordResetView.as_view(
        template_name="authentication/forgot_password.html",
        email_template_name="authentication/password_reset_email.html",
        from_email='%s'.format(DEFAULT_FROM_MAIL)), name='password_reset'),
    url(r'^reset-password/done/$', auth_views.PasswordResetDoneView.as_view(template_name="authentication/redirection_page.html"), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(template_name="authentication/set_password.html"), name='password_reset_confirm'),
    url(r'^reset-complete-done/$', auth_views.PasswordResetCompleteView.as_view(template_name="authentication/redirection_page.html"), name='password_reset_complete'),
]
