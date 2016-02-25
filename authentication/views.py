from django.shortcuts import render
from authentication.forms import LoginForm, ChangePasswordForm, SignUpForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.admin import User
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from website.settings import EMAIL_HOST_USER


def login_user(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
            else:
                error_message = 'Username or password is incorrect'
        else:
            error_message = 'Invalid input'
    else:
        form = LoginForm()

    return render(request, 'index.html', {'form': form,
                                          'error_message': error_message})


def logout_user(request):

    if request.user.is_authenticated:
        logout(request)

    return HttpResponseRedirect(reverse('index'))


def change_password(request):
    error_message = None
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            confirm_new_password = form.cleaned_data['confirm_new_password']
            if request.user.check_password(current_password) and new_password == confirm_new_password:
                request.user.set_password(new_password)
                request.user.save()
                return HttpResponseRedirect(reverse('change_password_done'))
            else:
                error_message = "Password does not match!"
        else:
            error_message = "Invalid input!"

    else:
        form = ChangePasswordForm()

    return render(request, 'change_password.html', {'form': form,
                                                    'error_message': error_message})


def change_password_done(request):
    return render(request, 'change_password_done.html')


def signup(request):
    error_message = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            try:
                user = User.objects.get(username=username)
                error_message = 'User already exists'
                return render(request, 'signup.html', {'form': form,
                                                       'error_message': error_message})
            except User.DoesNotExist:
                pass

            if '@stud.ntnu.no' in email or '@ntnu.no' in email:

                if password == confirm_password:

                    user = User.objects.create(username=username,
                                               email=email,
                                               first_name=first_name,
                                               last_name=last_name,
                                               password=password,)
                    user.save()
                    send_mail('Account verification',
                              'Link to activation',
                              '%s'.format(EMAIL_HOST_USER),
                              [email],
                              fail_silently=False)
                    return HttpResponseRedirect(reverse('signup_done'))
                else:
                    error_message = 'Password does not match'
                    return render(request, 'signup.html', {'form': form,
                                                           'error_message': error_message})
            else:
                error_message = 'You need to use an NTNU email'
                return render(request, 'signup.html',  {'form': form,
                                                        'error_message': error_message})

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form,
                                           'error_message': error_message})


def signup_done(request):
    return render(request, 'signup_done.html')