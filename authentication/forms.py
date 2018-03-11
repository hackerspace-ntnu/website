from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import User
from django.template.loader import render_to_string
# Note that default_token_generator is based on PasswordTokenGenerator
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from website.settings import DEFAULT_FROM_MAIL

default_error_messages = {'required': 'Feltet må fylles ut', 'invalid_choice': 'Verdien er ikke gyldig'}

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=50,
                                 label="Username",
                                 widget=forms.TextInput(),
                                 error_messages=default_error_messages)
    email = forms.CharField(max_length=50,
                                 label="Email",
                                 widget=forms.TextInput(),
                                 error_messages=default_error_messages)
    first_name = forms.CharField(max_length=50,
                                 label="First name",
                                 widget=forms.TextInput(),
                                 error_messages=default_error_messages)
    last_name = forms.CharField(max_length=50,
                                label="Last name",
                                widget=forms.TextInput(),
                                error_messages=default_error_messages)
    def clean_email(self):
        email = self.cleaned_data.get("email")
        # Checks if the email is already registered
        try:
            User.objects.get(email=email)
            message = 'Mailen er allerede registrert'
            self.add_error('email', message)
        except User.DoesNotExist:
            pass

        # Checks if the email is not from NTNU
        if not (str(email).endswith('@stud.ntnu.no') or str(email).endswith('@ntnu.no') or str(email).endswith(
                '@ntnu.edu')):
            message = 'Mailen er ikke fra NTNU'
            self.add_error('email', message)

        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")

        # Checks if user already exists
        try:
            User.objects.get(username=username)
            message = 'Brukernavnet eksisterer allerede'
            self.add_error('username', message)
        except User.DoesNotExist:
            pass

        return username

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data.get("email")
        user.is_active = False

        if commit:
            user.save()

        plain_message = render_to_string('signup_mail.txt', {
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user)}
        )
        html_message = render_to_string('signup_mail.html', {
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user)}
        )

        send_mail(
            'Velkommen som bruker hos Hackerspace',
            plain_message,
            DEFAULT_FROM_MAIL,
            [user.email],
            fail_silently=False,
            html_message=html_message
        )
        return user

