from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username", widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=100, label="Password", widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
