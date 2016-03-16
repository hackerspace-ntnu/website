from django.shortcuts import render
from authentication.forms import LoginForm, ChangePasswordForm, SignUpForm, ForgotPasswordForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.admin import User
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from website.settings import EMAIL_HOST_USER
from . import password_generate
from threading import Thread
import time
from django_user_agents.utils import get_user_agent


def login_user(request):
    user_agent = get_user_agent(request)
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

    context = {
        'form': form,
        'error_message': error_message,
        'mobile': user_agent.is_mobile,
    }

    return render(request, 'index.html', context)


def login_mobile(request):
    user_agent = get_user_agent(request)
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

    context = {
        'form': form,
        'error_message': error_message,
        'mobile': False,#user_agent.is_mobile,
    }

    return render(request, 'login_mobile.html', context)


def logout_user(request):

    if request.user.is_authenticated:
        logout(request)

    return HttpResponseRedirect(reverse('index'))


def change_password(request):
    user_agent = get_user_agent(request)
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

    context = {
        'form': form,
        'error_message': error_message,
        'mobile': user_agent.is_mobile,
    }
    return render(request, 'change_password.html', context)


def change_password_done(request):
    return render(request, 'change_password_done.html')


def signup(request):
    user_agent = get_user_agent(request)
    error_message = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = password_generate.generate_password()

            try:
                user = User.objects.get(username=username)
                error_message = 'Username already exists'
                context = {
                    'form': form,
                    'error_message': error_message,
                    'mobile': user_agent.is_mobile,
                }
                return render(request, 'signup.html', context)
            except User.DoesNotExist:
                pass

            try:
                user = User.objects.get(email=email)
                error_message = 'Email is already registered'
                context = {
                    'form': form,
                    'error_message': error_message,
                    'mobile': user_agent.is_mobile,
                }
                return render(request, 'signup.html', context)
            except User.DoesNotExist:
                pass

            if str(email).endswith('@stud.ntnu.no') or str(email).endswith('@ntnu.no'):

                user = User.objects.create(username=username,
                                           email=email,
                                           first_name=first_name,
                                           last_name=last_name,)
                user.set_password(password)
                user.save()

                email_subject = 'Account @ hackerspace NTNU'
                email_message = 'Congratulations! Your user is created. \n' +\
                                'Here is your insane secure password! \n' +\
                                'Password: {} \n'.format(password)
                thread = Thread(target=send_password_email, args=(email_subject, email_message, email))
                thread.start()

                return HttpResponseRedirect(reverse('signup_done'))

            else:
                error_message = 'You need to use an NTNU email'
                context = {
                    'form': form,
                    'error_message': error_message,
                    'mobile': user_agent.is_mobile,
                }
                return render(request, 'signup.html',  context)

    else:
        form = SignUpForm()

    context = {
        'form': form,
        'error_message': error_message,
        'mobile': user_agent.is_mobile,
    }
    return render(request, 'signup.html', context)


def send_password_email(subject, message, email):
    send_mail(subject,
              message,
              '%s'.format(EMAIL_HOST_USER),
              [email],
              fail_silently=False)


def signup_done(request):
    user_agent = get_user_agent(request)
    context = {
        'mobile': user_agent.is_mobile,
    }
    return render(request, 'signup_done.html', context)


def forgot_password(request):
    user_agent = get_user_agent(request)
    error_message = None
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                error_message = 'User does not exist'
                context = {
                    'form': form,
                    'error_message': error_message,
                    'mobile': user_agent.is_mobile,
                }
                return render(request, 'forgot_password.html', context)
            else:
                new_password = password_generate.generate_password()
                user.set_password(new_password)
                user.save()

                email_subject = 'New password @ hackerspace-ntnu.no'
                email_message = 'Here is your new password! \n' +\
                                'Password: {} \n'.format(new_password)
                thread = Thread(target=send_password_email, args=(email_subject, email_message, email))
                thread.start()

                return HttpResponseRedirect(reverse('forgot_password_done'))

        else:
            error_message = "Invalid input!"

    else:
        form = ForgotPasswordForm()

    context = {
        'form': form,
        'error_message': error_message,
        'mobile': user_agent.is_mobile,
    }
    return render(request, 'forgot_password.html', context)


def forgot_password_done(request):
    user_agent = get_user_agent(request)
    context = {
        'mobile': user_agent.is_mobile,
    }
    return render(request, 'forgot_password_done.html', context)
