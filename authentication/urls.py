from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from authentication.views import logout_user, SignUpView, SignUpDoneView, SignUpConfirmView
from website.settings import DEFAULT_FROM_MAIL

app_name = "authentication"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="authentication/login.html"), name='login'),
    path('logout/', logout_user, name='logout'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name="authentication/change_password.html", success_url="/authentication/change-password-done"), name='password_change'),
    path('change-password-done/', auth_views.PasswordChangeDoneView.as_view(template_name="authentication/redirection_page.html"), name='password_change_done'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup-done/', SignUpDoneView.as_view(), name='signup_done'),
    path('signup-confirm/<slug:uidb64>/<slug:token>/', SignUpConfirmView.as_view(), name='signup_confirm'),
    path('forgot-password/', auth_views.PasswordResetView.as_view(
        template_name="authentication/forgot_password.html",
        email_template_name="authentication/password_reset_email.html",
        success_url = '/authentication/reset-password/done',
        from_email='%s'.format(DEFAULT_FROM_MAIL)), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name="authentication/redirection_page.html"), name='password_reset_done'),
    path('reset/<slug:uidb64>/<slug:token>/', auth_views.PasswordResetConfirmView.as_view(template_name="authentication/set_password.html", success_url="/authentication/reset-complete-done/"), name='password_reset_confirm'),
    path('reset-complete-done/', auth_views.PasswordResetCompleteView.as_view(template_name="authentication/redirection_page.html"), name='password_reset_complete'),
]
