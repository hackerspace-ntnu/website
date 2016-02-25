from django import forms


class LoginForm(forms.Form):

    username = forms.CharField(max_length=100,
                               label="Username",
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=100,
                               label="Password",
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class ChangePasswordForm(forms.Form):

    current_password = forms.CharField(max_length=100,
                                       label="Current password",
                                       widget=forms.PasswordInput(attrs={'placeholder': 'Current password'}))
    new_password = forms.CharField(max_length=100,
                                   label="New password",
                                   widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_new_password = forms.CharField(max_length=100,
                                           label="Confirm password",
                                           widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class SignUpForm(forms.Form):

    username = forms.CharField(max_length=100,
                               label="Username",
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(max_length=100,
                             label="Email",
                             widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=50,
                                 label="First name",
                                 widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=50,
                                label="Last name",
                                widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    password = forms.CharField(max_length=100,
                               label="Password",
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(max_length=100,
                                       label="Confirm password",
                                       widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))
