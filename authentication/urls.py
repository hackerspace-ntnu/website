from django.conf.urls import url
from django.contrib.auth import views as auth_views
from authentication.views import logout_user, SignUpView, SignUpDoneView, SignUpConfirmView
from django.views.generic import RedirectView
from website.settings import DEFAULT_FROM_MAIL


urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^change-password/$', auth_views.PasswordChangeView.as_view(template_name="change_password.html"), name='password_change'),
    url(r'^change-password-done/$', auth_views.PasswordChangeDoneView.as_view(template_name="redirection_page.html"), name='password_change_done'),
    url(r'^signup/$', SignUpView, name='signup'),
    url(r'^signup-done/$', SignUpDoneView, name='signup_done'),
    url(r'^signup-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', SignUpConfirmView, name='signup_confirm'),
    url(r'^forgot-password/$', auth_views.PasswordResetView.as_view(
        template_name="forgot_password.html",
        email_template_name="password_reset_email.html",
        from_email='%s'.format(DEFAULT_FROM_MAIL)), name='password_reset'),
    url(r'^reset-password/done/$', auth_views.PasswordResetDoneView.as_view(template_name="redirection_page.html"), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(template_name="set_password.html"), name='password_reset_confirm'),
    url(r'^reset-complete-done/$', auth_views.PasswordResetCompleteView.as_view(template_name="redirection_page.html"), name='password_reset_complete'),
]
