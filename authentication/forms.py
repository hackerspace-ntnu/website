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
                                   widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
    confirm_new_password = forms.CharField(max_length=100,
                                           label="Confirm password",
                                           widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))

    def validate(self, user):
        current = self.cleaned_data["current_password"]
        new = self.cleaned_data["new_password"]
        confirm = self.cleaned_data["confirm_new_password"]

        if user.check_password(current) and new == confirm:
            return True
        else:
            return False


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
    new_password = forms.CharField(max_length=100,
                                   label="New password",
                                   widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
    confirm_new_password = forms.CharField(max_length=100,
                                           label="Confirm password",
                                           widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))


class ForgotPasswordForm(forms.Form):

    email = forms.EmailField(max_length=100,
                             label='Email',
                             widget=forms.TextInput(attrs={'placeholder': 'Email'}))


class SetPasswordForm(forms.Form):

    new_password = forms.CharField(max_length=100,
                                   label="New password",
                                   widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
    confirm_new_password = forms.CharField(max_length=100,
                                           label="Confirm password",
                                           widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    def password_matches(self):
        new_password = self.cleaned_data['new_password']
        confirm_new_password = self.cleaned_data['confirm_new_password']

        if new_password == confirm_new_password:
            return True
        else:
            return False


