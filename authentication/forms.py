from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.admin import User


default_error_messages = {'required': 'Feltet må fylles ut', 'invalid_choice': 'Verdien er ikke gyldig'}

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,
                               label="Username",
                               widget=forms.TextInput(),
                               error_messages=default_error_messages)
    password = forms.CharField(max_length=100,
                               label="Password",
                               widget=forms.PasswordInput(),
                               error_messages=default_error_messages)

    # Custom validation
    def validate(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)

        # Checks if user doesn't exist
        if user is None:
            message = 'Feil brukernavn eller passord'
            self.add_error('username', message)
            return False

        # Checks if the user is not active
        if not user.is_active:
            message = 'Brukeren er ikke aktivert'
            self.add_error('username', message)
            return False

        return True


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(max_length=100,
                                       label="Current password",
                                       widget=forms.PasswordInput(),
                                       error_messages=default_error_messages)
    new_password = forms.CharField(max_length=100,
                                   label="New password",
                                   widget=forms.PasswordInput(),
                                   error_messages=default_error_messages)
    confirm_new_password = forms.CharField(max_length=100,
                                           label="Confirm password",
                                           widget=forms.PasswordInput(),
                                           error_messages=default_error_messages)

    # Custom validation
    def validate(self, user):
        current = self.cleaned_data["current_password"]
        new = self.cleaned_data["new_password"]
        confirm = self.cleaned_data["confirm_new_password"]

        # Checks if the typed password doesn't match the current password
        if not user.check_password(current):
            message = "Nåværende passord er feil"
            self.add_error('current_password', message)
            return False

        # Checks if the new password and confirm new password doesn't match
        if not new == confirm:
            message = "De nye passordene er ikke like"
            self.add_error('current_password', message)
            return False
        return True


class SignUpForm(forms.Form):
    error_css_class = 'invalid'

    username = forms.CharField(max_length=100,
                               label="Username",
                               widget=forms.TextInput(attrs={'class' : 'validate' }),
                               error_messages=default_error_messages)
    email = forms.EmailField(max_length=100,
                             label="Email",
                             widget=forms.EmailInput(),
                             error_messages=default_error_messages)
    first_name = forms.CharField(max_length=50,
                                 label="First name",
                                 widget=forms.TextInput(attrs={'class' : 'validate' }),
                                 error_messages=default_error_messages)
    last_name = forms.CharField(max_length=50,
                                label="Last name",
                                widget=forms.TextInput(attrs={'class' : 'validate' }),
                                error_messages=default_error_messages)
    new_password = forms.CharField(max_length=100,
                                   label="New password",
                                   widget=forms.PasswordInput(),
                                   error_messages=default_error_messages)
    confirm_new_password = forms.CharField(max_length=100,
                                           label="Confirm password",
                                           widget=forms.PasswordInput(),
                                           error_messages=default_error_messages)

    # Custom validation
    def validate(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        new_password = self.cleaned_data['new_password']
        confirm_new_password = self.cleaned_data['confirm_new_password']

        # Checks if user already exists
        try:
            User.objects.get(username=username)
            message = 'Brukernavnet eksisterer allerede'
            self.add_error('username', message)
            self.fields['username'].widget=forms.TextInput(attrs={'class' : 'invalid' })
            return False
        except User.DoesNotExist:
            pass

        # Checks if the email is already registered
        try:
            User.objects.get(email=email)
            message = 'Mailen er allerede registrert'
            self.add_error('email', message)
            self.fields['email'].widget=forms.TextInput(attrs={'class' : 'invalid' })
            return False
        except User.DoesNotExist:
            pass

        # Checks if the email is not from NTNU
        if not (str(email).endswith('@stud.ntnu.no') or str(email).endswith('@ntnu.no') or str(email).endswith(
                '@ntnu.edu')):
            message = 'Mailen er ikke fra NTNU'
            self.add_error('email', message)
            self.fields['email'].widget=forms.TextInput(attrs={'class' : 'invalid' })
            return False

        # Checks if the new password and confirm new password doesn't match
        if not new_password == confirm_new_password:
            message = 'Passordene er ikke like'
            self.add_error('new_password', message)
            self.add_error('confirm_new_password', message)
            self.fields['new_password'].widget=forms.TextInput(attrs={'class' : 'invalid' })
            return False

        return True



class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=100,
                             label='Email',
                             widget=forms.TextInput(),
                             error_messages=default_error_messages)

    # Custom validation
    def validate(self):
        email = self.cleaned_data['email']

        # Checks if the user with email exist
        try:
            User.objects.get(email=email)
            return True
        except User.DoesNotExist:
            message = "Mailen er ikke registrert"
            self.add_error("email", message)
            return False


class SetPasswordForm(forms.Form):
    new_password = forms.CharField(max_length=100,
                                   label="New password",
                                   widget=forms.PasswordInput(),
                                   error_messages=default_error_messages)
    confirm_new_password = forms.CharField(max_length=100,
                                           label="Confirm password",
                                           widget=forms.PasswordInput(),
                                           error_messages=default_error_messages)

    # Custom validation
    def validate(self):
        new_password = self.cleaned_data['new_password']
        confirm_new_password = self.cleaned_data['confirm_new_password']

        # Checks if the new password and confirm new password doesn't match
        if not new_password == confirm_new_password:
            message = "Passordene er ikke like"
            self.add_error('new_password', message)
            self.add_error('confirm_new_password', message)
            return False
        return True
