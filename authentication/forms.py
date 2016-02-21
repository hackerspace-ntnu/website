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
